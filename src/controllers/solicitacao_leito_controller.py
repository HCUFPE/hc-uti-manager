from typing import List, Dict, Any, Optional
from datetime import timedelta
from fastapi import HTTPException
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.historico_provider import HistoricoProvider
from sqlalchemy import select
from models.leito_estado import LeitoEstado

class SolicitacaoLeitoController:
    """
    Controller para gerenciar solicitações de vaga/leito na UTI.
    """

    def __init__(
        self, 
        leito_provider: SolicitacaoLeitoProvider, 
        estado_provider: LeitoEstadoProvider | None = None,
        historico_provider: HistoricoProvider | None = None,
        aghu_cirurgia_provider: Any = None
    ):
        self.leito_provider = leito_provider
        self.estado_provider = estado_provider
        self.historico_provider = historico_provider
        self.aghu_cirurgia_provider = aghu_cirurgia_provider

    async def _sincronizar_prioridades(self, data_cirurgia: str, turno: str, sol_id_foco: int | None = None, prioridade_desejada: str | None = None):
        """
        Garante que a fila de prioridades seja contínua (P1, P2, P3...) e sem buracos.
        Ordena com base na hora de início da cirurgia e na data de criação como desempate.
        """
        if not data_cirurgia or not turno:
            return

        # 1. Busca todas as solicitações Pendentes para esse bucket
        todas = await self.leito_provider.get_todas()
        bucket = [s for s in todas if s.data_cirurgia == data_cirurgia and s.turno == turno and s.status == "Pendente"]
        
        if not bucket:
            return

        # 2. Define a ordem base: Hora da Cirurgia crescente (default: "99:99") e Data de Criação
        def obter_peso(s):
            hora = s.hora_cirurgia if s.hora_cirurgia else "99:99"
            criado = s.criado_em.timestamp() if s.criado_em else 0
            return (hora, criado)

        bucket.sort(key=obter_peso)

        # 3. Reatribui P1, P2, P3... sequencialmente para todos no bucket
        for i, sol in enumerate(bucket):
            nova_prio = f"P{i+1}"
            if sol.prioridade != nova_prio:
                await self.leito_provider.atualizar(sol.id, {"prioridade": nova_prio})


    async def listar_solicitacoes(self) -> List[Dict[str, Any]]:
        """Retorna todas as solicitações de leito ativas."""
        solicitacoes = await self.leito_provider.get_todas()
        
        return [
            {
                "id": str(s.id),
                "prontuario": s.prontuario,
                "nome": s.nome,
                "idade": s.idade,
                "especialidade": s.especialidade,
                "procedimento": s.procedimento,
                "tipo": s.tipo,
                "status": s.status,
                "turno": s.turno,
                "data_cirurgia": s.data_cirurgia,
                "hora_cirurgia": s.hora_cirurgia,
                "prioridade": s.prioridade,
                "perfil_solicitante": s.perfil_solicitante,
                "destino": s.destino,
                "cirurgia_finalizada": bool(s.cirurgia_finalizada),
                "encaminhamento_liberado": bool(s.encaminhamento_liberado),
                "dataHora": (s.criado_em - timedelta(hours=3)).strftime("%Y-%m-%d %H:%M") if s.criado_em else "",
            }
            for s in solicitacoes
        ]

    async def criar_solicitacao(self, payload: dict) -> dict:
        """Registra uma nova solicitação de leito utilizando dados importados do AGHU."""
        prontuario = payload.get("prontuario")
        if not prontuario:
            raise HTTPException(status_code=400, detail="O prontuário é obrigatório.")

        # 1. Consultar dados do paciente/cirurgia no AGHU
        dados_aghu = await self.consultar_dados_aghu(str(prontuario))

        dt = dados_aghu["data_cirurgia"]
        trn = dados_aghu["turno"]
        nome = dados_aghu["nome"]
        idade = dados_aghu["idade"]
        especialidade = dados_aghu["especialidade"] or "GERAL"
        procedimento = dados_aghu["procedimento"]
        hora_cirurgia = dados_aghu["hora_cirurgia"]

        nova_solicitacao_data = {
            "prontuario": str(prontuario),
            "nome": nome,
            "idade": idade,
            "especialidade": especialidade,
            "procedimento": procedimento,
            "tipo": payload.get("tipo"),
            "turno": trn,
            "data_cirurgia": dt,
            "hora_cirurgia": hora_cirurgia,
            "status": "Pendente",
            "perfil_solicitante": payload.get("perfil_solicitante")
        }

        # 2. Cria a solicitação no banco local
        sol = await self.leito_provider.criar(nova_solicitacao_data)
        
        # 3. Sincroniza a fila de prioridades para esse dia/turno
        await self._sincronizar_prioridades(dt, trn)
        
        return {"message": "Solicitação de leito registrada com sucesso."}

    async def atualizar_status(self, sol_id: int, payload: dict) -> dict:
        """Atualiza o status ou o destino de uma solicitação."""
        alvo = await self.leito_provider.get_por_id(sol_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

        dados = {}
        if "status" in payload:
            dados["status"] = payload["status"]
        if "destino" in payload:
            dados["destino"] = payload["destino"]
            if payload.get("status") is None:
                dados["status"] = "Reservado"

        await self.leito_provider.atualizar(sol_id, dados)
        
        # Se mudou status, a fila desse dia/turno pode ter buracos
        await self._sincronizar_prioridades(alvo.data_cirurgia, alvo.turno)
        
        return {"message": "Solicitação atualizada."}

    async def editar_solicitacao(self, sol_id: int, payload: dict, user_perfil: str = "") -> dict:
        """
        Permite editar os dados de uma solicitação.
        """
        alvo = await self.leito_provider.get_por_id(sol_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        if alvo.status != "Pendente":
            perfis_permitidos = ["BC", "BC-Admin", "COB", "COB-Admin", "HEM", "HEM-Admin", "Administrador"]
            if alvo.status == "Reservado" and user_perfil in perfis_permitidos:
                pass # Permite a edição
            else:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Não é possível editar uma solicitação com status '{alvo.status}'. Cancele a reserva primeiro."
                )

        # Campos que podem ser editados
        campos_validos = ["prontuario", "idade", "especialidade", "tipo", "turno", "data_cirurgia", "prioridade", "nome", "procedimento", "hora_cirurgia"]
        dados_atualizar = {k: v for k, v in payload.items() if k in campos_validos}
        
        # Se mudou o prontuário, busca os novos dados no AGHU
        if "prontuario" in payload and str(payload["prontuario"]) != str(alvo.prontuario):
            dados_aghu = await self.consultar_dados_aghu(str(payload["prontuario"]))
            dados_atualizar.update({
                "prontuario": str(payload["prontuario"]),
                "nome": dados_aghu["nome"],
                "idade": dados_aghu["idade"],
                "especialidade": dados_aghu["especialidade"] or "GERAL",
                "procedimento": dados_aghu["procedimento"],
                "data_cirurgia": dados_aghu["data_cirurgia"],
                "hora_cirurgia": dados_aghu["hora_cirurgia"],
                "turno": dados_aghu["turno"]
            })
        
        if not dados_atualizar:
            raise HTTPException(status_code=400, detail="Nenhum campo válido para atualização fornecido.")

        # Salva o bucket antigo para caso mude data/turno
        old_dt = alvo.data_cirurgia
        old_trn = alvo.turno

        # Atualiza
        await self.leito_provider.atualizar(sol_id, dados_atualizar)
        
        if alvo.status == "Reservado" and self.estado_provider:
            new_prontuario = dados_atualizar.get("prontuario", alvo.prontuario)
            try:
                new_prontuario_int = int(new_prontuario) if new_prontuario else None
            except (ValueError, TypeError):
                new_prontuario_int = None
                
            new_idade = dados_atualizar.get("idade", alvo.idade)
            new_especialidade = dados_atualizar.get("especialidade", alvo.especialidade)
            
            await self.estado_provider.atualizar_dados_reserva_por_solicitacao(
                sol_id=sol_id,
                prontuario=new_prontuario_int,
                idade=new_idade,
                especialidade=new_especialidade
            )
        
        # Sincroniza o novo bucket
        new_dt = dados_atualizar.get("data_cirurgia", old_dt)
        new_trn = dados_atualizar.get("turno", old_trn)
        new_prio = dados_atualizar.get("prioridade", alvo.prioridade)
        
        await self._sincronizar_prioridades(new_dt, new_trn, sol_id_foco=sol_id, prioridade_desejada=new_prio)
        
        # Se mudou de bucket, sincroniza o antigo também para tapar o buraco
        if new_dt != old_dt or new_trn != old_trn:
            await self._sincronizar_prioridades(old_dt, old_trn)

        return {"message": "Solicitação editada com sucesso."}

    async def cancelar_solicitacao(self, sol_id: int, user_perfil: str = "") -> dict:
        """Cancela uma solicitação de leito."""
        alvo = await self.leito_provider.get_por_id(sol_id)
        if not alvo:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        if alvo.status != "Pendente":
            perfis_permitidos = ["BC", "BC-Admin", "COB", "COB-Admin", "HEM", "HEM-Admin", "Administrador"]
            if alvo.status == "Reservado" and user_perfil in perfis_permitidos:
                if self.estado_provider:
                    await self.estado_provider.limpar_reserva_por_solicitacao(sol_id)
            else:
                raise HTTPException(
                    status_code=403, 
                    detail=f"Não é possível cancelar uma solicitação com status '{alvo.status}'. Cancele a reserva primeiro."
                )
            
        dt, trn = alvo.data_cirurgia, alvo.turno
        sucesso = await self.leito_provider.deletar(sol_id)
        
        if sucesso:
            # Sincroniza para tapar o buraco
            await self._sincronizar_prioridades(dt, trn)
            
        return {"message": "Solicitação cancelada."}

    async def reservar_leito(self, sol_id: int, leito_id: str) -> dict:
        """
        Vincula uma solicitação pendente a um leito específico.
        """
        solicitacao = await self.leito_provider.get_por_id(sol_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        dt, trn = solicitacao.data_cirurgia, solicitacao.turno

        # 1. Verificar se o leito já possui uma reserva ativa
        result_existente = await self.estado_provider.session.execute(
            select(LeitoEstado).where(LeitoEstado.lto_id == leito_id)
        )
        estado_existente = result_existente.scalar_one_or_none()
        if estado_existente and estado_existente.prontuario_proximo and estado_existente.solicitacao_id != sol_id:
            raise HTTPException(status_code=400, detail=f"O leito {leito_id} já possui uma reserva ativa.")

        # 2. Registrar a reserva no estado local do leito
        await self.estado_provider.salvar_reserva(
            lto_id=leito_id,
            prontuario=int(solicitacao.prontuario),
            idade=solicitacao.idade,
            especialidade=solicitacao.especialidade,
            solicitacao_id=solicitacao.id
        )

        # 2. Atualizar a solicitação original
        await self.leito_provider.atualizar(sol_id, {
            "status": "Reservado",
            "destino": f"Leito {leito_id}"
        })

        # 3. Sincroniza a fila (um saiu da fila, os outros sobem)
        await self._sincronizar_prioridades(dt, trn)

        return {"message": f"Reserva do leito {leito_id} realizada com sucesso."}

    async def cancelar_reserva(self, sol_id: int) -> dict:
        """
        Remove o vínculo entre a solicitação e o leito, 
        voltando o status para 'Pendente'.
        """
        solicitacao = await self.leito_provider.get_por_id(sol_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")

        dt, trn = solicitacao.data_cirurgia, solicitacao.turno

        # 1. Limpar a reserva no leito (SQLite)
        await self.estado_provider.limpar_reserva_por_solicitacao(sol_id)

        # 2. Voltar a solicitação para Pendente
        await self.leito_provider.atualizar(sol_id, {
            "status": "Pendente",
            "destino": None
        })

        # 3. Sincroniza a fila (um voltou, pode empurrar outros)
        await self._sincronizar_prioridades(dt, trn, sol_id_foco=sol_id, prioridade_desejada=solicitacao.prioridade)

        return {"message": "Reserva cancelada. Solicitação voltou para Pendente."}

    async def marcar_cirurgia_finalizada(self, sol_id: int) -> dict:
        """Marca que a cirurgia do paciente foi finalizada."""
        sol = await self.leito_provider.get_por_id(sol_id)
        if not sol:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
        await self.leito_provider.atualizar(sol_id, {"cirurgia_finalizada": True})
        return {"message": "Cirurgia finalizada com sucesso."}

    async def liberar_encaminhamento(self, sol_id: int) -> dict:
        """Autoriza o encaminhamento do paciente para a UTI."""
        sol = await self.leito_provider.get_por_id(sol_id)
        if not sol:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
        await self.leito_provider.atualizar(sol_id, {"encaminhamento_liberado": True})
        return {"message": "Encaminhamento liberado com sucesso."}

    async def cancelar_liberacao(self, sol_id: int) -> dict:
        """Revoga a liberação de encaminhamento do paciente para a UTI."""
        sol = await self.leito_provider.get_por_id(sol_id)
        if not sol:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
        await self.leito_provider.atualizar(sol_id, {"encaminhamento_liberado": False})
        return {"message": "Liberação de encaminhamento cancelada."}

    async def remanejar_reserva(self, sol_id: int, novo_leito_id: str) -> dict:
        """
        Altera o leito de destino reservado de uma solicitação para um novo leito disponível.
        """
        solicitacao = await self.leito_provider.get_por_id(sol_id)
        if not solicitacao:
            raise HTTPException(status_code=404, detail="Solicitação não encontrada.")
            
        if solicitacao.status != "Reservado":
            raise HTTPException(status_code=400, detail="Apenas solicitações com status 'Reservado' podem ser remanejadas.")
            
        # Verificar se o leito de destino já tem uma reserva
        result_destino = await self.estado_provider.session.execute(
            select(LeitoEstado).where(LeitoEstado.lto_id == novo_leito_id)
        )
        estado_destino = result_destino.scalar_one_or_none()
        if estado_destino and estado_destino.prontuario_proximo and estado_destino.solicitacao_id != sol_id:
            raise HTTPException(status_code=400, detail=f"O leito {novo_leito_id} já possui uma reserva ativa.")
            
        # Realizar a transferência de reserva
        old_lto_id = await self.estado_provider.transferir_reserva(sol_id, novo_leito_id)
        if not old_lto_id:
            raise HTTPException(status_code=400, detail="Não foi possível identificar o leito de origem da reserva atual.")
            
        # Atualizar o destino na solicitação original
        await self.leito_provider.atualizar(sol_id, {"destino": f"Leito {novo_leito_id}"})
        
        return {
            "message": f"Reserva remanejada com sucesso do Leito {old_lto_id} para o Leito {novo_leito_id}.",
            "leito_origem": old_lto_id,
            "leito_destino": novo_leito_id,
            "prontuario": solicitacao.prontuario
        }

    async def consultar_dados_aghu(self, prontuario: str) -> dict:
        """Consulta as informações do paciente e da cirurgia no AGHU.

        Args:
            prontuario (str): Prontuário do paciente.

        Returns:
            dict: Informações mapeadas e formatadas do paciente/cirurgia.
        """
        import os
        from datetime import datetime

        data_cirurgia_aghu = None
        
        # Tenta buscar do AGHU
        if self.aghu_cirurgia_provider:
            try:
                data_cirurgia_aghu = await self.aghu_cirurgia_provider.obter_cirurgia_por_prontuario(prontuario)
            except Exception as e:
                # Log e continua para fallback se estiver em desenvolvimento
                print(f"Erro ao acessar AGHU DB: {e}")
                
        # Fallback mock em desenvolvimento caso não encontre ou esteja sem conexão
        if not data_cirurgia_aghu:
            if os.getenv("MOCK_BEDS") == "true" or not self.aghu_cirurgia_provider:
                # Gerar dados simulados para testes locais
                hoje_str = datetime.today().strftime("%d-%m-%Y")
                mocks = {
                    "77": {
                        "Prontuário": 77,
                        "Nome Completo": "MANOEL SEVERINO DOS SANTOS",
                        "Data de Nascimento": "15-05-1927",
                        "Data da Cirurgia": hoje_str,
                        "Hora de Início": "08:30",
                        "Especialidade": "CCP (CABEÇA E PESCOÇO)",
                        "Procedimento Principal": "TIREOIDECTOMIA PARCIAL"
                    },
                    "123": {
                        "Prontuário": 123,
                        "Nome Completo": "ANA MARIA SILVA",
                        "Data de Nascimento": "10-10-1992",
                        "Data da Cirurgia": hoje_str,
                        "Hora de Início": "14:15",
                        "Especialidade": "TORÁCICA",
                        "Procedimento Principal": "LOBECTOMIA PULMONAR"
                    },
                    "1": {
                        "Prontuário": 1,
                        "Nome Completo": "TESTE PACIENTE 1",
                        "Data de Nascimento": "25-05-2017",
                        "Data da Cirurgia": hoje_str,
                        "Hora de Início": "20:00",
                        "Especialidade": "PROCTOLOGIA",
                        "Procedimento Principal": "HEMORROIDECTOMIA"
                    }
                }
                
                if prontuario in mocks:
                    data_cirurgia_aghu = mocks[prontuario]
                else:
                    # Gera um paciente fictício dinâmico para qualquer outro prontuário digitado em testes
                    data_cirurgia_aghu = {
                        "Prontuário": int(prontuario) if prontuario.isdigit() else 999,
                        "Nome Completo": f"PACIENTE TESTE {prontuario}",
                        "Data de Nascimento": "25-05-1980",
                        "Data da Cirurgia": hoje_str,
                        "Hora de Início": "09:00",
                        "Especialidade": "GERAL",
                        "Procedimento Principal": "LAPAROSCOPIA DIAGNOSTICA"
                    }
            
        if not data_cirurgia_aghu:
            raise HTTPException(
                status_code=404, 
                detail="Nenhuma cirurgia programada ativa encontrada para este prontuário no AGHU."
            )

        # Processar dados
        nome = data_cirurgia_aghu.get("Nome Completo")
        dt_nascimento_str = data_cirurgia_aghu.get("Data de Nascimento")
        especialidade = data_cirurgia_aghu.get("Especialidade")
        procedimento = data_cirurgia_aghu.get("Procedimento Principal")
        data_cirurgia_br = data_cirurgia_aghu.get("Data da Cirurgia")
        hora_inicio = data_cirurgia_aghu.get("Hora de Início")
        
        # Calcular idade
        idade = 0
        if dt_nascimento_str:
            try:
                birth_date = datetime.strptime(dt_nascimento_str, "%d-%m-%Y")
                today = datetime.today()
                idade = today.year - birth_date.year - ((today.month, today.day) < (birth_date.month, birth_date.day))
            except Exception:
                pass
                
        # Mapear turno
        turno = "Manhã"
        if hora_inicio:
            try:
                parts = hora_inicio.split(":")
                hour = int(parts[0])
                if 7 <= hour < 13:
                    turno = "Manhã"
                elif 13 <= hour < 19:
                    turno = "Tarde"
                else:
                    turno = "Noite"
            except Exception:
                pass

        # Converter data da cirurgia de DD-MM-YYYY para YYYY-MM-DD para consistência com o banco e frontend
        data_cirurgia_db = None
        if data_cirurgia_br:
            try:
                if "-" in data_cirurgia_br:
                    parts = data_cirurgia_br.split("-")
                    if len(parts) == 3:
                        if len(parts[0]) == 4: # Já está em YYYY-MM-DD
                            data_cirurgia_db = data_cirurgia_br
                        else:
                            data_cirurgia_db = f"{parts[2]}-{parts[1]}-{parts[0]}"
                else:
                    data_cirurgia_db = data_cirurgia_br
            except Exception:
                data_cirurgia_db = data_cirurgia_br
                
        return {
            "prontuario": str(prontuario),
            "nome": nome,
            "idade": idade,
            "especialidade": especialidade,
            "procedimento": procedimento,
            "data_cirurgia": data_cirurgia_db,
            "hora_cirurgia": hora_inicio,
            "turno": turno
        }

