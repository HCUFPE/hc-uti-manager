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

    def __init__(self, alerta_provider: AlertaProvider, leitos_controller: Any, alta_provider: SolicitacaoAltaProvider, solicitacao_leito_provider: SolicitacaoLeitoProvider, historico_provider: Any = None):
        self.alerta_provider = alerta_provider
        self.leitos_controller = leitos_controller
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
        try:
            novos_alertas_data = []
            hoje_bsb = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d")
            
            # 1. Analisar Leitos
            leitos = await self.leitos_controller.listar_leitos()
            
            # 2. Analisar Solicitações de Alta
            await self._analisar_altas(novos_alertas_data)

            # 3. Analisar Histórico (Notificações Bidirecionais)
            await self._analisar_historico(novos_alertas_data, hoje_bsb)

            # 4. Sincronização e Limpeza
            return await self._sincronizar_alertas(novos_alertas_data)

        except Exception as e:
            logger.exception("Erro crítico na geração de alertas")
            return {"message": "Erro ao processar alertas.", "error": str(e)}

    async def _analisar_altas(self, novos_alertas: List[Dict[str, Any]]):
        try:
            leitos = await self.leitos_controller.listar_leitos()
            leitos_map = {l["lto_lto_id"]: l for l in leitos}
            altas = await self.alta_provider.get_todas()
            
            for alta in altas:
                if alta.status == "pendente":
                    leito_info = leitos_map.get(alta.lto_id, {})
                    prontuario = alta.prontuario
                    
                    # Tenta recuperar prontuário de leitos mockados se estiver N/D
                    if (prontuario == "N/D" or not prontuario) and leito_info.get("prontuario_atual"):
                        prontuario = str(leito_info["prontuario_atual"])

                    novos_alertas.append({
                        "tipo": "aviso",
                        "categoria": "Gargalo",
                        "titulo": "Solicitação de Alta",
                        "mensagem": f"Aguardando destino para leito {alta.lto_id} (Prontuário {prontuario}).",
                        "lto_id": alta.lto_id,
                        "prontuario": str(prontuario),
                        "perfil_alvo": "NIR",
                        "criado_em": alta.criado_em
                    })
                    
                    if alta.leito_destino and len(str(alta.leito_destino).strip()) > 1:
                        novos_alertas.append({
                            "tipo": "info",
                            "categoria": "Gargalo",
                            "titulo": "Acomodação Definida",
                            "mensagem": f"Destino definido para paciente {prontuario}: {alta.leito_destino}.",
                            "lto_id": alta.lto_id,
                            "prontuario": str(prontuario),
                            "perfil_alvo": None,
                            "criado_em": alta.atualizado_em
                        })
        except Exception as e:
            logger.error(f"Erro ao analisar altas: {e}")

    async def _analisar_historico(self, novos_alertas: List[Dict[str, Any]], hoje_bsb: str):
        if not self.historico_provider:
            return

        try:
            vagas = await self.solicitacao_leito_provider.get_todas()
            limite_24h = datetime.utcnow() - timedelta(hours=24)
            eventos = await self.historico_provider.listar(limit=300)
            eventos_recentes = [e for e in eventos if e.get("criado_em") and e.get("criado_em") > limite_24h]
            
            for ev in eventos_recentes:
                self._processar_evento_historico(ev, vagas, novos_alertas, hoje_bsb)
        except Exception as e:
            logger.error(f"Erro ao analisar histórico: {e}")

    def _processar_evento_historico(self, ev, vagas, novos_alertas, hoje_bsb):
        tipo = ev.get("tipo")
        detalhes = ev.get("detalhes", "")
        operador = ev.get("operador", "Sistema")
        criado_em_evento = ev.get("criado_em")
        prontuario_evento = ev.get("prontuario")
        
        if "Teste" in detalhes:
            return

        is_alta_event = "Alta #" in detalhes or tipo in ["alta", "cancelamento", "alteracao_destino", "destino_disponivel", "destino_pendente"]

        # Parsing de ID
        sid = None
        s_match = re.search(r'#(\d+)', detalhes)
        vaga = None
        if s_match and not is_alta_event:
            try:
                sid = int(s_match.group(1))
                vaga = next((v for v in vagas if v.id == sid), None)
            except: pass

        p_match = re.search(r'Prontu[^\s]*\s+(\w+)', detalhes, re.IGNORECASE)
        pront_alerta = p_match.group(1) if p_match else (prontuario_evento or "Desconhecido")
        
        match_hoje = self._validar_data_hoje(detalhes, vaga, hoje_bsb)

        if vaga:
            pront_alerta = str(vaga.prontuario)
            perfil_vaga = vaga.perfil_solicitante
        else:
            perfil_vaga = None

        # Lógica de Alertas por Tipo
        self._gerar_alerta_por_tipo(tipo, detalhes, operador, criado_em_evento, pront_alerta, perfil_vaga, match_hoje, novos_alertas)

    def _validar_data_hoje(self, detalhes, vaga, hoje_bsb) -> bool:
        d_sol = None
        if vaga:
            d_sol = str(vaga.data_cirurgia).strip()
            if "/" in d_sol:
                p = d_sol.split("/")
                if len(p) == 3: d_sol = f"{p[2]}-{p[1]}-{p[0]}"
            elif " " in d_sol: d_sol = d_sol.split(" ")[0]
            elif "T" in d_sol: d_sol = d_sol.split("T")[0]
        else:
            d_match = re.search(r'Data:\s+([\d/-]+)', detalhes)
            if d_match:
                d_sol = d_match.group(1).strip()
                if "/" in d_sol:
                    p = d_sol.split("/")
                    if len(p) == 3: d_sol = f"{p[2]}-{p[1]}-{p[0]}"
        
        return d_sol == hoje_bsb

    def _gerar_alerta_por_tipo(self, tipo, detalhes, operador, criado_em_evento, pront_alerta, perfil_vaga, match_hoje, novos_alertas):
        # 1. UTI <-> SOLICITANTE
        if tipo in ["reserva", "cancelamento_reserva"]:
            op_clean = operador.replace("-Admin", "").strip().upper()
            pv_clean = str(perfil_vaga or "").replace("-Admin", "").strip().upper()
            
            if perfil_vaga:
                if tipo == "reserva":
                    novos_alertas.append({
                        "tipo": "info", "categoria": "Gargalo", "titulo": "Vaga Reservada pela UTI",
                        "mensagem": detalhes, "prontuario": pront_alerta, "perfil_alvo": perfil_vaga, "criado_em": criado_em_evento
                    })
                elif tipo == "cancelamento_reserva" and op_clean != pv_clean:
                    novos_alertas.append({
                        "tipo": "info", "categoria": "Gargalo", "titulo": "Reserva Cancelada pela UTI",
                        "mensagem": detalhes, "prontuario": pront_alerta, "perfil_alvo": perfil_vaga, "criado_em": criado_em_evento
                    })
            
            if tipo == "cancelamento_reserva" and perfil_vaga and op_clean == pv_clean:
                novos_alertas.append({
                    "tipo": "aviso", "categoria": "Gargalo", "titulo": "Solicitante cancelou a reserva",
                    "mensagem": detalhes, "prontuario": pront_alerta, "perfil_alvo": None, "criado_em": criado_em_evento
                })

        # 2. SOLICITANTE -> UTI
        elif tipo in ["nova_solicitacao", "exclusao_solicitacao", "alteracao_prioridade"]:
            if match_hoje:
                titulos = {
                    "nova_solicitacao": "Nova solicitação para hoje",
                    "exclusao_solicitacao": "Solicitação para hoje removida",
                    "alteracao_prioridade": "Prioridade alterada (Paciente hoje)"
                }
                novos_alertas.append({
                    "tipo": "info", "categoria": "Gargalo", "titulo": titulos.get(tipo),
                    "mensagem": detalhes, "prontuario": pront_alerta, "perfil_alvo": None, "criado_em": criado_em_evento
                })
        
        # 3. UTI -> NIR ou NIR -> UTI
        elif tipo == "cancelamento":
            if "pelo NIR" in detalhes:
                novos_alertas.append({
                    "tipo": "aviso",
                    "categoria": "Gargalo",
                    "titulo": "Cancelamento de Alta pelo NIR",
                    "mensagem": detalhes,
                    "prontuario": pront_alerta,
                    "perfil_alvo": None,  # Alvo: UTI
                    "criado_em": criado_em_evento
                })
            else:
                novos_alertas.append({
                    "tipo": "aviso",
                    "categoria": "Gargalo",
                    "titulo": "Alta Cancelada pela UTI",
                    "mensagem": detalhes,
                    "prontuario": pront_alerta,
                    "perfil_alvo": "NIR",
                    "criado_em": criado_em_evento
                })

        # 4. NIR -> UTI (Destino)
        elif tipo in ["alteracao_destino", "destino_disponivel", "destino_pendente"]:
            titulos = {
                "alteracao_destino": "Destino de Alta Definido",
                "destino_disponivel": "Leito de Destino LIBERADO",
                "destino_pendente": "Liberação de Destino CANCELADA"
            }
            tipos_alerta = {
                "alteracao_destino": "info",
                "destino_disponivel": "aviso",
                "destino_pendente": "critico"
            }
            novos_alertas.append({
                "tipo": tipos_alerta.get(tipo, "info"), 
                "categoria": "Gargalo", 
                "titulo": titulos.get(tipo),
                "mensagem": detalhes, 
                "prontuario": pront_alerta, 
                "perfil_alvo": None, # Alvo: UTI
                "criado_em": criado_em_evento
            })

        # 5. Fluxo de Encaminhamento Cirúrgico (Solicitante <-> UTI)
        elif tipo in ["cirurgia_finalizada", "encaminhamento_liberado", "encaminhamento_cancelado"]:
            if tipo == "cirurgia_finalizada":
                novos_alertas.append({
                    "tipo": "aviso",
                    "categoria": "Gargalo",
                    "titulo": "Cirurgia Finalizada",
                    "mensagem": f"Prontuário {pront_alerta} pronto para ser encaminhado para UTI (Cirurgia Finalizada)",
                    "prontuario": pront_alerta,
                    "perfil_alvo": None, # Alvo: UTI
                    "criado_em": criado_em_evento
                })
            elif tipo == "encaminhamento_liberado":
                novos_alertas.append({
                    "tipo": "info",
                    "categoria": "Gargalo",
                    "titulo": "Encaminhamento Autorizado",
                    "mensagem": f"Paciente do prontuário {pront_alerta} pode ser encaminhado para a UTI.",
                    "prontuario": pront_alerta,
                    "perfil_alvo": perfil_vaga, # Alvo: Solicitante (COB, BC, HEM)
                    "criado_em": criado_em_evento
                })
            elif tipo == "encaminhamento_cancelado":
                novos_alertas.append({
                    "tipo": "critico",
                    "categoria": "Gargalo",
                    "titulo": "Liberação de Encaminhamento Cancelada",
                    "mensagem": f"A liberação de encaminhamento para o prontuário {pront_alerta} foi cancelada pela UTI.",
                    "prontuario": pront_alerta,
                    "perfil_alvo": perfil_vaga, # Alvo: Solicitante (COB, BC, HEM)
                    "criado_em": criado_em_evento
                })

    async def _sincronizar_alertas(self, novos_alertas_data: List[Dict[str, Any]]) -> dict:
        alertas_existentes = await self.alerta_provider.get_todos()
        alertas_manter_ids = []
        chaves_ja_processadas = set()
        
        for data in novos_alertas_data:
            ts_str = data.get("criado_em").isoformat() if data.get("criado_em") else "now"
            chave = f"{data.get('titulo')}|{data.get('prontuario')}|{data.get('perfil_alvo')}|{data.get('mensagem')}|{ts_str}"
            
            if chave in chaves_ja_processadas:
                continue
            
            existente = None
            for a in alertas_existentes:
                if (a.titulo == data.get("titulo") and 
                    str(a.prontuario) == str(data.get("prontuario")) and
                    a.perfil_alvo == data.get("perfil_alvo") and
                    a.mensagem == data.get("mensagem")):
                    
                    req_criado_em = data.get("criado_em")
                    if req_criado_em:
                        if a.criado_em and abs((a.criado_em - req_criado_em).total_seconds()) < 2:
                            existente = a
                            break
                    else:
                        existente = a
                        break
            
            if existente:
                alertas_manter_ids.append(existente.id)
            else:
                novo = await self.alerta_provider.criar(data)
                alertas_manter_ids.append(novo.id)
            
            chaves_ja_processadas.add(chave)

        # Limpeza de obsoletos desativada para manter histórico completo de alertas
        # for a_antigo in alertas_existentes:
        #     if a_antigo.id not in alertas_manter_ids:
        #         if a_antigo.categoria in ["Infeccioso", "Permanencia", "Limpeza"]:
        #             await self.alerta_provider.deletar(a_antigo.id)

        return {"message": f"{len(novos_alertas_data)} alertas processados."}
