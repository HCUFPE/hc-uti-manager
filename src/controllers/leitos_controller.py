from models.reserva_leito import ReservaLeitoInput
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import asyncio
import os

import logging

logger = logging.getLogger(__name__)

class LeitosController:
    def __init__(self, census_provider, estado_provider, alta_provider=None, solicitacao_provider=None):
        self.census_provider = census_provider
        self.estado_provider = estado_provider
        self.alta_provider = alta_provider
        self.solicitacao_provider = solicitacao_provider

    def _calcular_idade(self, data_nasc) -> int | None:
        if not data_nasc:
            return None
        try:
            if isinstance(data_nasc, str):
                for fmt in ("%Y-%m-%d", "%d/%m/%Y"):
                    try:
                        nascimento = datetime.strptime(data_nasc, fmt).date()
                        break
                    except ValueError:
                        continue
                else:
                    return None
            elif isinstance(data_nasc, (date, datetime)):
                nascimento = data_nasc
            else:
                return None

            hoje = date.today()
            return hoje.year - nascimento.year - (
                (hoje.month, hoje.day) < (nascimento.month, nascimento.day)
            )
        except Exception:
            return None

    async def listar_leitos(self) -> List[Dict[str, Any]]:
        # 1. Busca o censo (Realidade do Hospital)
        leitos = []
        try:
            leitos = await self.census_provider.listar_leitos()
        except Exception as e:
            logger.error(f"Erro ao buscar censo: {e}")
            leitos = []
            
        # Injeção de leitos de teste via variável de ambiente para flexibilidade
        if os.getenv("ENV") == "development" and os.getenv("MOCK_BEDS") == "true":
            logger.info("Injetando leitos de teste (Mock)...")
            mock_beds = [
                {"lto_lto_id": "UTI-01", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None},
                {"lto_lto_id": "UTI-02", "status": "Ocupado", "tipo": "uti", "prontuario_atual": "999999", "nome_atual": "PACIENTE TESTE ALTA", "idade_atual": 45, "especialidade_atual": "CARDIOLOGIA"},
                {"lto_lto_id": "UTI-03", "status": "Ocupado", "tipo": "uti", "prontuario_atual": "123456", "nome_atual": "PACIENTE ATUAL", "prontuario_proximo": "987654", "nome_proximo": "PACIENTE CHEGANDO"},
                {"lto_lto_id": "UTI-04", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None},
            ]
            
            # Evita duplicados se o AGHU já retornou algum desses IDs (embora improvável com nomes tipo UTI-01)
            ids_existentes = {str(l.get('lto_lto_id')).strip().upper() for l in leitos}
            for mb in mock_beds:
                if mb["lto_lto_id"] not in ids_existentes:
                    leitos.append(mb)
            
        # 2. Busca estados locais (Reservas)
        try:
            estados = await self.estado_provider.obter_estados()
        except Exception as e:
            logger.error(f"Erro ao buscar estados locais: {e}")
            estados = {}

        # 3. Busca solicitações de alta
        altas_map = {}
        if self.alta_provider:
            try:
                raw_altas = await self.alta_provider.obter_altas_map()
                # Normaliza chaves para garantir merge (ex: 'uti-01' -> 'UTI-01')
                altas_map = {str(k).strip().upper(): v for k, v in raw_altas.items()}
            except Exception as e:
                logger.error(f"Erro ao buscar mapa de altas: {e}")
        
        # 3b. Mapeia onde cada prontuário está no AGHU para detecção de "paciente chegou em outro leito"
        census_map = {} # prontuario -> lto_id
        for l in leitos:
            p = l.get('prontuario_atual')
            if p: census_map[str(p).strip()] = str(l.get('lto_lto_id', '')).strip().upper()

        # 4. Merge
        for leito in leitos:
            # Normaliza o ID para evitar erros de comparação (ex: 'UTI-01 ' vs 'UTI-01')
            raw_lto_id = leito.get('lto_lto_id', '')
            lto_id = str(raw_lto_id).strip().upper()
            leito['lto_lto_id'] = lto_id 
            
            if 'data_nascimento' in leito:
                leito['idade_atual'] = self._calcular_idade(leito['data_nascimento'])
            
            # Altas
            if lto_id in altas_map:
                alta_obj = altas_map[lto_id]
                leito['alta_solicitada'] = True
                leito['alta_info'] = alta_obj.to_dict()
                leito['leito_destino'] = alta_obj.leito_destino
                leito['destino_disponivel'] = bool(alta_obj.destino_disponivel)
            else:
                leito['leito_destino'] = None
                leito['destino_disponivel'] = False
                
                if lto_id in estados:
                    leito['alta_solicitada'] = estados[lto_id].alta_solicitada
                else:
                    leito['alta_solicitada'] = leito.get('alta_solicitada', False)

            # Reservas e Sincronização Inteligente
            if lto_id in estados:
                est = estados[lto_id]
                prontuario_reserva = str(est.prontuario_proximo or "").strip()
                
                # SUCESSO/CONCLUSÃO: O paciente reservado apareceu no AGHU (neste leito ou em outro)
                if prontuario_reserva and prontuario_reserva in census_map:
                    try:
                        lto_aghu_real = census_map[prontuario_reserva]
                        # Se ele chegou, não importa o leito, limpamos a reserva deste leito (lto_id)
                        await self.estado_provider.limpar_reserva(lto_id)
                        
                        sol_id = getattr(est, 'solicitacao_id', None)
                        if sol_id and self.solicitacao_provider:
                            await self.solicitacao_provider.atualizar(sol_id, {"status": "Concluída"})
                        
                        leito['prontuario_proximo'] = None
                        leito['conflito_reserva'] = False
                        
                        if lto_aghu_real != lto_id:
                            logger.info(f"Paciente {prontuario_reserva} reservado para {lto_id} mas chegou no {lto_aghu_real}. Reserva liberada.")
                    except Exception as e:
                        logger.error(f"Erro na sincronização inteligente do leito {lto_id}: {e}")
                else:
                    # Se não apareceu no AGHU ainda, verificamos CONFLITO (outro paciente ocupou o leito reservado)
                    prontuario_aghu_neste_leito = leito.get('prontuario_atual')
                    if prontuario_aghu_neste_leito and prontuario_reserva:
                        # Alguém ocupou o leito e não é quem reservamos
                        is_alta = leito.get('alta_solicitada', False)
                        leito['conflito_reserva'] = not is_alta
                    else:
                        leito['conflito_reserva'] = False
                        
                    leito['prontuario_proximo'] = est.prontuario_proximo
                    leito['idade_proximo'] = est.idade_proximo
                    leito['especialidade_proximo'] = est.especialidade_proximo
                    
                    # Busca info da cirurgia
                    sol_id = getattr(est, 'solicitacao_id', None)
                    if sol_id and self.solicitacao_provider:
                        sol = await self.solicitacao_provider.get_por_id(sol_id)
                        if sol:
                            leito['data_cirurgia_proximo'] = sol.data_cirurgia
                            leito['turno_proximo'] = sol.turno
            else:
                leito['conflito_reserva'] = False
                leito['prontuario_proximo'] = None
                leito['idade_proximo'] = None
                leito['especialidade_proximo'] = None
        return leitos

    async def listar(self):
        return await self.listar_leitos()

    async def reservar(self, lto_lto_id: str, payload: ReservaLeitoInput):
        await self.estado_provider.salvar_reserva(
            lto_id=lto_lto_id,
            prontuario=payload.prontuario,
            idade=payload.idade,
            especialidade=payload.especialidade
        )
        return {"message": "Reserva registrada com sucesso"}

    async def cancelar_reserva(self, lto_id: str, solicitacao_provider: Any = None):
        """
        Limpa a reserva de um leito e, se houver uma solicitação vinculada, 
        retorna o status dela para 'Pendente'.
        """
        # 1. Limpar reserva no estado local e obter dados vinculados
        dados_reserva = await self.estado_provider.limpar_reserva(lto_id)
        sol_id = dados_reserva.get("sol_id")
        prontuario = dados_reserva.get("prontuario")
        solicitacao = None
        
        # 2. Se temos o ID e o provider, restauramos a solicitação na fila
        if sol_id and solicitacao_provider:
            solicitacao = await solicitacao_provider.atualizar(sol_id, {
                "status": "Pendente",
                "destino": None
            })
            
        return {
            "message": f"Reserva do leito {lto_id} cancelada.",
            "solicitacao": solicitacao,
            "prontuario": prontuario
        }
    
    async def solicitar_alta(self, leito_id: str):
        """
        Versão compatível com a rota legada de leitos.
        Cria uma solicitação no novo sistema de Altas.
        """
        if self.alta_provider:
            # Busca prontuário atual
            leitos = await self.census_provider.listar_leitos()
            leito_info = next((l for l in leitos if l['lto_lto_id'] == leito_id), None)
            prontuario = str(leito_info['prontuario_atual']) if leito_info and leito_info.get('prontuario_atual') else "N/D"
            
            await self.alta_provider.criar({
                "lto_id": leito_id,
                "prontuario": prontuario,
                "status": "pendente"
            })
        
        # Também mantém no estado legado para garantir visibilidade em queries antigas se houver
        await self.estado_provider.salvar_alta(leito_id, True)

    async def cancelar_alta(self, leito_id: str):
        if self.alta_provider:
            solicitacao = await self.alta_provider.get_por_lto_id(leito_id)
            if solicitacao:
                await self.alta_provider.atualizar(solicitacao.id, {"status": "cancelada"})
        
        await self.estado_provider.salvar_alta(leito_id, False) 

    async def listar_leitos_disponiveis_para_reserva(self):
        leitos = await self.listar_leitos()
        
        # Termos que o AGHU usa para leitos vazios
        status_vazios = ['DESOCUPADO', 'DISPONIVEL', 'DISPONÍVEL', 'VAGO', 'LIBERADO', 'LIMPEZA', 'VAGO/LIMPO', 'HIGIENIZACAO', 'HIGIENIZAÇÃO']
        
        disponiveis = []
        for l in leitos:
            status = str(l.get('status', '')).strip().upper()
            status_local = str(l.get('status_local', '')).strip().upper()
            prontuario_atual = l.get('prontuario_atual')
            proximo_paciente = l.get('prontuario_proximo')
            tem_alta = l.get('alta_solicitada', False)
            
            # Um leito está disponível para reserva se:
            # 1. Não tem reserva já feita (proximo_paciente é nulo ou vazio)
            # 2. E (está fisicamente vago OU tem status de vazio OU tem alta solicitada)
            
            if status == "DESATIVADO":
                continue
                
            ja_tem_reserva = proximo_paciente is not None and str(proximo_paciente).strip() != ""
            esta_fisicamente_vazio = (prontuario_atual is None or str(prontuario_atual).strip() in ["", "0", "N/D"])
            
            if not ja_tem_reserva:
                if esta_fisicamente_vazio or (status in status_vazios) or (status_local in status_vazios) or tem_alta:
                    disponiveis.append(l)
        
        return disponiveis
