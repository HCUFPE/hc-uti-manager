from typing import List, Dict, Any
from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
import logging
import re

from providers.implementations.alerta_provider import AlertaProvider
from providers.interfaces.leito_provider_interface import LeitoProviderInterface
from providers.implementations.solicitacao_alta_provider import SolicitacaoAltaProvider
from providers.implementations.solicitacao_leito_provider import SolicitacaoLeitoProvider

logger = logging.getLogger(__name__)

class AlertaController:
    """
    Controller para gerenciar a lógica de negócio dos alertas do sistema.
    """

    def __init__(
        self, 
        alerta_provider: AlertaProvider,
        census_provider: LeitoProviderInterface,
        alta_provider: SolicitacaoAltaProvider,
        solicitacao_leito_provider: SolicitacaoLeitoProvider,
        historico_provider: Any = None
    ):
        self.alerta_provider = alerta_provider
        self.census_provider = census_provider
        self.alta_provider = alta_provider
        self.solicitacao_leito_provider = solicitacao_leito_provider
        self.historico_provider = historico_provider

    async def listar_alertas(self, perfil_usuario: str = None) -> List[Dict[str, Any]]:
        """
        Retorna os alertas filtrados pelo perfil do usuário diretamente do banco local.
        """
        alertas = await self.alerta_provider.get_todos()
        
        if not perfil_usuario:
            return []
            
        if perfil_usuario == "Administrador":
            return [a.to_dict() for a in alertas]
        
        user_grupo = perfil_usuario.replace("-Admin", "").strip()
        
        if user_grupo == "UTI":
            return [a.to_dict() for a in alertas if a.perfil_alvo is None]
            
        return [a.to_dict() for a in alertas if a.perfil_alvo == user_grupo]

    async def atualizar_status_leitura(self, alerta_id: int, lido: bool) -> dict:
        """Atualiza o status de leitura de um alerta."""
        alerta = await self.alerta_provider.atualizar(alerta_id, {"lido": lido})
        if not alerta:
            raise HTTPException(status_code=404, detail="Alerta não encontrado.")
        return {"message": "Status do alerta atualizado com sucesso."}

    async def marcar_todos_como_lidos(self, perfil_usuario: str) -> dict:
        """Marca todos os alertas do perfil como lidos no banco de dados."""
        alertas_atuais = await self.listar_alertas(perfil_usuario)
        for a in alertas_atuais:
            if not a.get("lido"):
                await self.alerta_provider.atualizar(int(a["id"]), {"lido": True})
        return {"message": "Todos os alertas marcados como lidos"}

    async def gerar_alertas(self) -> dict:
        """
        Analisa o estado atual do sistema e gera novos alertas.
        """
        alertas_existentes = await self.alerta_provider.get_todos()
        novos_alertas_data = []
        hoje_bsb = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d")
        
        # 1. Analisar Leitos (Desativado conforme solicitado: Infeccioso, Permanência, Limpeza)
        # O loop foi mantido vazio caso queira adicionar novas lógicas de leitos no futuro
        try:
            leitos_aghu = await self.census_provider.listar_leitos()
            for leito in leitos_aghu:
                pass
        except Exception as e:
            logger.error(f"Erro ao analisar leitos: {e}")
        except Exception as e:
            logger.error(f"Erro ao analisar leitos: {e}")

        # 2. Analisar Solicitações de Alta
        try:
            altas = await self.alta_provider.get_todas()
            for alta in altas:
                if alta.status == "pendente":
                    novos_alertas_data.append({
                        "tipo": "aviso",
                        "categoria": "Gargalo",
                        "titulo": "Solicitação de Alta",
                        "mensagem": f"Aguardando destino para leito {alta.lto_id} (Prontuário {alta.prontuario}).",
                        "lto_id": alta.lto_id,
                        "prontuario": str(alta.prontuario),
                        "perfil_alvo": "NIR"
                    })
                    
                    if alta.leito_destino and len(str(alta.leito_destino).strip()) > 1:
                        novos_alertas_data.append({
                            "tipo": "info",
                            "categoria": "Gargalo",
                            "titulo": "Acomodação Definida",
                            "mensagem": f"Destino definido para paciente {alta.prontuario}: {alta.leito_destino}.",
                            "lto_id": alta.lto_id,
                            "prontuario": str(alta.prontuario),
                            "perfil_alvo": None 
                        })
        except Exception as e:
            logger.error(f"Erro ao analisar altas: {e}")

        # 3. Analisar Histórico (Notificações Bidirecionais)
        try:
            vagas = await self.solicitacao_leito_provider.get_todas()
            if self.historico_provider:
                # Janela de 24h: permite ver o que aconteceu durante a noite/ontem
                limite_24h = datetime.utcnow() - timedelta(hours=24)
                eventos = await self.historico_provider.listar(limit=300)
                eventos_recentes = [e for e in eventos if e.get("criado_em") and e.get("criado_em") > limite_24h]
                
                for ev in eventos_recentes:
                    tipo = ev.get("tipo")
                    detalhes = ev.get("detalhes", "")
                    operador = ev.get("operador", "Sistema")
                    criado_em_evento = ev.get("criado_em")
                    vaga = None 
                    
                    if "Alta #" in detalhes or "Teste" in detalhes:
                        continue

                    # Tentar pegar ID da solicitação/alta do texto (#ID)
                    sid = None
                    s_match = re.search(r'#(\d+)', detalhes)
                    if s_match:
                        try:
                            sid = int(s_match.group(1))
                            vaga = next((v for v in vagas if v.id == sid), None)
                        except: pass

                    p_match = re.search(r'Prontu[^\s]*\s+(\w+)', detalhes, re.IGNORECASE)
                    pront_alerta = p_match.group(1) if p_match else "Desconhecido"
                    perfil_vaga = None
                    match_hoje = False

                    if vaga:
                        pront_alerta = str(vaga.prontuario)
                        perfil_vaga = vaga.perfil_solicitante
                        d_sol = str(vaga.data_cirurgia).strip()
                        if "/" in d_sol:
                            p = d_sol.split("/")
                            if len(p) == 3: d_sol = f"{p[2]}-{p[1]}-{p[0]}"
                        elif " " in d_sol:
                            d_sol = d_sol.split(" ")[0]
                        elif "T" in d_sol:
                            d_sol = d_sol.split("T")[0]
                        
                        if d_sol == hoje_bsb:
                            match_hoje = True
                    else:
                        d_match = re.search(r'Data:\s+([\d/-]+)', detalhes)
                        if d_match:
                            d_sol = d_match.group(1).strip()
                            if "/" in d_sol:
                                p = d_sol.split("/")
                                if len(p) == 3: d_sol = f"{p[2]}-{p[1]}-{p[0]}"
                            if d_sol == hoje_bsb:
                                match_hoje = True

                    # 1. UTI <-> SOLICITANTE (Reserva e Cancelamento de Reserva)
                    if tipo in ["reserva", "cancelamento_reserva"]:
                        op_clean = operador.replace("-Admin", "").strip().upper()
                        pv_clean = str(perfil_vaga or "").replace("-Admin", "").strip().upper()
                        
                        if perfil_vaga:
                            if tipo == "reserva":
                                novos_alertas_data.append({
                                    "tipo": "info",
                                    "categoria": "Gargalo",
                                    "titulo": "Vaga Reservada pela UTI",
                                    "mensagem": detalhes,
                                    "prontuario": pront_alerta,
                                    "perfil_alvo": perfil_vaga,
                                    "criado_em": criado_em_evento
                                })
                            elif tipo == "cancelamento_reserva" and op_clean != pv_clean:
                                novos_alertas_data.append({
                                    "tipo": "info",
                                    "categoria": "Gargalo",
                                    "titulo": "Reserva Cancelada pela UTI",
                                    "mensagem": detalhes,
                                    "prontuario": pront_alerta,
                                    "perfil_alvo": perfil_vaga,
                                    "criado_em": criado_em_evento
                                })
                        
                        if tipo == "cancelamento_reserva" and perfil_vaga and op_clean == pv_clean:
                            novos_alertas_data.append({
                                "tipo": "aviso",
                                "categoria": "Gargalo",
                                "titulo": "Solicitante cancelou a reserva",
                                "mensagem": detalhes,
                                "prontuario": pront_alerta,
                                "perfil_alvo": None, # UTI
                                "criado_em": criado_em_evento
                            })

                    # 2. SOLICITANTE -> ALERTA UTI (Nova Solicitação/Exclusão/Prioridade hoje)
                    elif tipo in ["nova_solicitacao", "exclusao_solicitacao", "alteracao_prioridade"]:
                        if match_hoje:
                            titulo = "Nova solicitação para hoje"
                            if tipo == "exclusao_solicitacao": 
                                titulo = "Solicitação para hoje removida"
                            elif tipo == "alteracao_prioridade": 
                                titulo = "Prioridade alterada (Paciente hoje)"
                            
                            novos_alertas_data.append({
                                "tipo": "info",
                                "categoria": "Gargalo",
                                "titulo": titulo,
                                "mensagem": detalhes,
                                "prontuario": pront_alerta,
                                "perfil_alvo": None, # UTI
                                "criado_em": criado_em_evento
                            })
                    
                    # 3. UTI -> NIR (Cancelamento de Alta)
                    elif tipo == "cancelamento":
                        novos_alertas_data.append({
                            "tipo": "aviso",
                            "categoria": "Gargalo",
                            "titulo": "Alta Cancelada pela UTI",
                            "mensagem": detalhes,
                            "prontuario": pront_alerta,
                            "perfil_alvo": "NIR",
                            "criado_em": criado_em_evento
                        })
        except Exception as e:
            logger.error(f"Erro ao analisar histórico: {e}")

        # 4. Sincronização Final com Deduplicação Dinâmica
        alertas_manter_ids = []
        chaves_ja_processadas = set()
        
        for data in novos_alertas_data:
            # Chave agora inclui o timestamp para evitar que eventos diferentes mas com mesma mensagem sejam mesclados
            ts_str = data.get("criado_em").isoformat() if data.get("criado_em") else "now"
            chave = f"{data.get('titulo')}|{data.get('prontuario')}|{data.get('perfil_alvo')}|{data.get('mensagem')}|{ts_str}"
            
            if chave in chaves_ja_processadas:
                continue
            
            existente = next((a for a in alertas_existentes if 
                             a.titulo == data.get("titulo") and 
                             str(a.prontuario) == str(data.get("prontuario")) and
                             a.perfil_alvo == data.get("perfil_alvo") and
                             a.mensagem == data.get("mensagem") and
                             (a.criado_em == data.get("criado_em") if data.get("criado_em") else True)), None)
            
            if existente:
                alertas_manter_ids.append(existente.id)
            else:
                novo = await self.alerta_provider.criar(data)
                alertas_manter_ids.append(novo.id)
            
            chaves_ja_processadas.add(chave)

        # 5. Limpeza de obsoletos (apenas alertas automáticos do AGHU, não os do histórico)
        for a_antigo in alertas_existentes:
            if a_antigo.id not in alertas_manter_ids:
                if a_antigo.categoria in ["Infeccioso", "Permanencia", "Limpeza"]:
                    await self.alerta_provider.deletar(a_antigo.id)

        return {"message": f"{len(novos_alertas_data)} alertas processados."}
