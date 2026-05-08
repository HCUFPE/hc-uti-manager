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
        
        if not perfil_usuario or perfil_usuario == "Administrador":
            return []
        
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
        # 1. Inicialização segura de variáveis para evitar NameError
        alertas_existentes = await self.alerta_provider.get_todos()
        novos_alertas_data = []
        vagas = []
        altas = []
        hoje_bsb = (datetime.now() - timedelta(hours=3)).strftime("%Y-%m-%d")
        
        # 1. Analisar Leitos (Infeccioso, Permanência, Limpeza)
        try:
            leitos_aghu = await self.census_provider.listar_leitos()
            for leito in leitos_aghu:
                lto_id = leito.get("lto_lto_id")
                nome_pac = leito.get("nome_paciente", "Desconhecido")
                observacao = str(leito.get("observacao") or "").upper()
                
                if any(bac in observacao for bac in ["KPC", "VRE", "ACINETOBACTER", "MRSA", "CONTATO"]):
                    novos_alertas_data.append({
                        "tipo": "critico",
                        "categoria": "Infeccioso",
                        "titulo": f"Precaução de Contato ({'KPC' if 'KPC' in observacao else 'Multirresistente'})",
                        "mensagem": f"Leito {lto_id} ({nome_pac}) com indicação de isolamento/precaução.",
                        "lto_id": lto_id,
                        "prontuario": str(leito.get("prontuario_atual")) if leito.get("prontuario_atual") else None
                    })

                tempo_ocupacao = leito.get("tempo_ocupacao")
                if tempo_ocupacao and isinstance(tempo_ocupacao, int) and tempo_ocupacao > 21:
                    novos_alertas_data.append({
                        "tipo": "aviso",
                        "categoria": "Permanencia",
                        "titulo": "Permanência Prolongada (> 21 dias)",
                        "mensagem": f"Leito {lto_id} ({nome_pac}) com {tempo_ocupacao} dias na UTI.",
                        "lto_id": lto_id,
                        "prontuario": str(leito.get("prontuario_atual")) if leito.get("prontuario_atual") else None
                    })

                if leito.get("status") == "LIMPEZA":
                     novos_alertas_data.append({
                        "tipo": "info",
                        "categoria": "Limpeza",
                        "titulo": "Leito em Higienização",
                        "mensagem": f"Leito {lto_id} encontra-se no status LIMPEZA.",
                        "lto_id": lto_id
                    })
        except Exception as e:
            logger.error(f"Erro ao analisar leitos: {e}")

        # 2. Analisar Solicitações de Alta
        try:
            altas = await self.alta_provider.get_todas()
            for alta in altas:
                if alta.status == "pendente":
                    # Alerta para o NIR
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

        # 3. Analisar Solicitações de Vaga e Histórico para UTI
        try:
            vagas = await self.solicitacao_leito_provider.get_todas()
            if self.historico_provider:
                # Janela de 24 horas para não perder nada
                limite_24h = datetime.utcnow() - timedelta(hours=24)
                eventos = await self.historico_provider.listar(limit=200)
                eventos_recentes = [e for e in eventos if e.get("criado_em") and e.get("criado_em") > limite_24h]
                
                for ev in eventos_recentes:
                    tipo = ev.get("tipo")
                    detalhes = ev.get("detalhes", "")
                    
                    if "Alta #" in detalhes or "Teste" in detalhes:
                        continue

                    # Localizar paciente da vaga correspondente
                    vaga = None
                    match_hoje = False
                    pront_alerta = None
                    if "Prontu" in detalhes:
                        try:
                            # Regex flexível para capturar o número após "Prontuário", "Prontuario", etc.
                            p_match = re.search(r'Prontu[^\s]*\s+(\w+)', detalhes, re.IGNORECASE)
                            if p_match:
                                pront_hist = p_match.group(1).strip()
                                vaga = next((v for v in vagas if str(v.prontuario).strip() == pront_hist), None)
                        except: pass

                    if vaga and vaga.data_cirurgia:
                        d_sol = str(vaga.data_cirurgia).strip()
                        if "/" in d_sol:
                            p = d_sol.split("/")
                            if len(p) == 3: d_sol = f"{p[2]}-{p[1]}-{p[0]}"
                        elif "T" in d_sol:
                            d_sol = d_sol.split("T")[0]
                        
                        if d_sol == hoje_bsb:
                            match_hoje = True
                            pront_alerta = str(vaga.prontuario)
                    else:
                        # Se a vaga foi excluída, tentamos pegar a data direto do histórico
                        try:
                            d_match = re.search(r'Data:\s+([\d/-]+)', detalhes)
                            if d_match:
                                d_sol = d_match.group(1).strip()
                                if "/" in d_sol:
                                    p = d_sol.split("/")
                                    if len(p) == 3: d_sol = f"{p[2]}-{p[1]}-{p[0]}"
                                
                                if d_sol == hoje_bsb:
                                    match_hoje = True
                                    # Pegar prontuário também via regex se não tiver vaga
                                    p_match = re.search(r'Prontu[^\s]*\s+(\w+)', detalhes, re.IGNORECASE)
                                    pront_alerta = p_match.group(1) if p_match else "Desconhecido"
                        except: pass

                    if match_hoje:
                        titulo = "Uma nova solicitação de leito foi inserida com data de cirurgia prevista para o dia atual"
                        if tipo == "exclusao_solicitacao": 
                            titulo = "Uma solicitação de leito para o dia atual foi removida da lista"
                        elif tipo == "alteracao_prioridade": 
                            titulo = "A ordem de prioridade de um paciente agendado para hoje foi alterada"
                        
                        novos_alertas_data.append({
                            "tipo": "info",
                            "categoria": "Gargalo",
                            "titulo": titulo,
                            "mensagem": detalhes,
                            "prontuario": pront_alerta,
                            "perfil_alvo": None 
                        })
        except Exception as e:
            logger.error(f"Erro ao analisar vagas/histórico: {e}")

        # 4. Sincronização Final com o Banco
        alertas_manter_ids = []
        for data in novos_alertas_data:
            # Unicidade por Título + Prontuário + Perfil
            existente = next((a for a in alertas_existentes if 
                             a.titulo == data.get("titulo") and 
                             str(a.prontuario) == str(data.get("prontuario")) and
                             a.perfil_alvo == data.get("perfil_alvo")), None)
            
            if existente:
                alertas_manter_ids.append(existente.id)
            else:
                novo = await self.alerta_provider.criar(data)
                alertas_manter_ids.append(novo.id)

        # 5. Limpeza de obsoletos (apenas categorias de estado)
        for a_antigo in alertas_existentes:
            if a_antigo.id not in alertas_manter_ids:
                if a_antigo.categoria in ["Infeccioso", "Permanencia", "Limpeza"]:
                    await self.alerta_provider.deletar(a_antigo.id)

        return {"message": f"{len(novos_alertas_data)} alertas processados."}
