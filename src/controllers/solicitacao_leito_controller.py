from typing import List, Dict, Any, Optional
from datetime import timedelta
from fastapi import HTTPException
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider
from providers.implementations.leito_estado_provider import LeitoEstadoProvider
from providers.implementations.historico_provider import HistoricoProvider

class SolicitacaoLeitoController:
    """
    Controller para gerenciar solicitações de vaga/leito na UTI.
    """

    def __init__(
        self, 
        leito_provider: SolicitacaoLeitoProvider, 
        estado_provider: LeitoEstadoProvider | None = None,
        historico_provider: HistoricoProvider | None = None
    ):
        self.leito_provider = leito_provider
        self.estado_provider = estado_provider
        self.historico_provider = historico_provider

    async def _sincronizar_prioridades(self, data_cirurgia: str, turno: str, sol_id_foco: int | None = None, prioridade_desejada: str | None = None):
        """
        Garante que a fila de prioridades seja contínua (P1, P2, P3...) e sem buracos.
        Se prioridade_desejada for informada para sol_id_foco, tenta posicioná-lo ali e remaneja os outros.
        """
        if not data_cirurgia or not turno:
            return

        # 1. Busca todas as solicitações Pendentes para esse bucket
        todas = await self.leito_provider.get_todas()
        bucket = [s for s in todas if s.data_cirurgia == data_cirurgia and s.turno == turno and s.status == "Pendente"]
        
        if not bucket:
            return

        # 2. Define a ordem base
        def obter_peso(s):
            # Se for o cara que estamos editando/criando agora e ele quer uma prioridade específica
            if s.id == sol_id_foco and prioridade_desejada:
                # Usamos um timestamp negativo (-1) para ele ganhar o desempate na mesma prioridade
                return (int(prioridade_desejada[1:]), -1)
            
            # Se já tem prioridade, usa ela. Se não, vai pro final da fila (peso 999)
            try:
                prio_val = int(s.prioridade[1:]) if s.prioridade and s.prioridade.startswith('P') else 999
            except:
                prio_val = 999
            return (prio_val, s.criado_em.timestamp() if s.criado_em else 0)

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
                "idade": s.idade,
                "especialidade": s.especialidade,
                "tipo": s.tipo,
                "status": s.status,
                "turno": s.turno,
                "data_cirurgia": s.data_cirurgia,
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
        """Registra uma nova solicitação de leito."""
        dt = payload.get("data_cirurgia")
        trn = payload.get("turno")
        prio = payload.get("prioridade")

        nova_solicitacao_data = {
            "prontuario": payload.get("prontuario"),
            "idade": payload.get("idade"),
            "especialidade": payload.get("especialidade"),
            "tipo": payload.get("tipo"),
            "turno": trn,
            "data_cirurgia": dt,
            "prioridade": prio,
            "status": "Pendente",
            "perfil_solicitante": payload.get("perfil_solicitante")
        }

        if not all([nova_solicitacao_data["prontuario"], nova_solicitacao_data["idade"], nova_solicitacao_data["especialidade"]]):
             raise HTTPException(status_code=400, detail="Campos obrigatorios ausentes.")

        # Cria a solicitação
        sol = await self.leito_provider.criar(nova_solicitacao_data)
        
        # Sincroniza a fila para esse dia/turno
        await self._sincronizar_prioridades(dt, trn, sol_id_foco=sol.id, prioridade_desejada=prio)
        
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
        campos_validos = ["prontuario", "idade", "especialidade", "tipo", "turno", "data_cirurgia", "prioridade"]
        dados_atualizar = {k: v for k, v in payload.items() if k in campos_validos}
        
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

        # 1. Registrar a reserva no estado local do leito
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
