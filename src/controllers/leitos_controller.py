from models.reserva_leito import ReservaLeitoInput
from typing import List, Dict, Any, Optional
from datetime import date, datetime
import asyncio
import os

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
        try:
            leitos = await self.census_provider.listar_leitos()
            # Injeção manual de leitos de teste para desenvolvimento
            if os.getenv("ENV") == "development":
                leitos.extend([
                    {"lto_lto_id": "UTI-01", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None},
                    {"lto_lto_id": "UTI-02", "status": "Ocupado", "tipo": "uti", "prontuario_atual": "999999", "nome_atual": "PACIENTE TESTE ALTA", "idade_atual": 45, "especialidade_atual": "CARDIOLOGIA"},
                    {"lto_lto_id": "UTI-03", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None},
                    {"lto_lto_id": "UTI-04", "status": "Desocupado", "tipo": "uti", "prontuario_atual": None},
                ])
        except Exception as e:
            print(f"Erro ao buscar censo: {e}")
            leitos = []
            
        # 2. Busca estados locais (Reservas)
        try:
            estados = await self.estado_provider.obter_estados()
        except Exception as e:
            print(f"Erro ao buscar estados: {e}")
            estados = {}

        # MESCLA LEITOS DE TESTE (Apenas em ambiente de desenvolvimento)
        if os.getenv("ENV") == "development":
            pass
            
        # 3. Busca solicitações de alta
        altas_map = {}
        if self.alta_provider:
            try:
                altas_map = await self.alta_provider.obter_altas_map()
            except Exception as e:
                print(f"Erro ao buscar altas: {e}")
        
        # 4. Merge
        for leito in leitos:
            # Normaliza o ID para evitar erros de comparação (ex: 'UTI-01 ' vs 'UTI-01')
            raw_lto_id = leito.get('lto_lto_id', '')
            lto_id = str(raw_lto_id).strip().upper()
            leito['lto_lto_id'] = lto_id # Atualiza o ID no objeto para o padrão limpo
            
            if 'data_nascimento' in leito:
                leito['idade_atual'] = self._calcular_idade(leito['data_nascimento'])
            
            # Prioridade para a nova tabela de solicitações de alta
            if lto_id in altas_map:
                leito['alta_solicitada'] = True
                leito['alta_info'] = altas_map[lto_id].to_dict()
            else:
                # Fallback para o booleano simples se existir no estado_provider (legado/suporte)
                if lto_id in estados:
                    leito['alta_solicitada'] = estados[lto_id].alta_solicitada
                else:
                    leito['alta_solicitada'] = leito.get('alta_solicitada', False)

            # Reservas e Sincronização
            if lto_id in estados:
                est = estados[lto_id]
                
                prontuario_aghu = leito.get('prontuario_atual')
                prontuario_reserva = est.prontuario_proximo
                
                # Se o leito foi ocupado no AGHU e havia uma reserva
                if prontuario_aghu and prontuario_reserva:
                    try:
                        if str(prontuario_aghu) == str(prontuario_reserva):
                            # SUCESSO: O paciente reservado chegou!
                            await self.estado_provider.limpar_reserva(lto_id)
                            sol_id = getattr(est, 'solicitacao_id', None)
                            if sol_id and self.solicitacao_provider:
                                await self.solicitacao_provider.atualizar(sol_id, {"status": "Concluída"})
                            
                            leito['prontuario_proximo'] = None
                        else:
                            # Só é CONFLITO se não houver uma alta já planejada para o paciente atual
                            is_alta = leito.get('alta_solicitada', False)
                            
                            if not is_alta:
                                leito['conflito_reserva'] = True
                            else:
                                leito['conflito_reserva'] = False
                                
                            leito['prontuario_proximo'] = est.prontuario_proximo
                            leito['idade_proximo'] = est.idade_proximo
                            leito['especialidade_proximo'] = est.especialidade_proximo
                            
                            # Busca info da cirurgia para exibir no card
                            sol_id = getattr(est, 'solicitacao_id', None)
                            if sol_id and self.solicitacao_provider:
                                sol = await self.solicitacao_provider.get_por_id(sol_id)
                                if sol:
                                    leito['data_cirurgia_proximo'] = sol.data_cirurgia
                                    leito['turno_proximo'] = sol.turno
                    except Exception as e:
                        print(f"Erro na sincronização do leito {lto_id}: {e}")
                        leito['prontuario_proximo'] = est.prontuario_proximo
                else:
                    # Sem conflito, mantém a exibição da reserva normal
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
        # 1. Limpar reserva no estado local e obter o ID da solicitação vinculada
        sol_id = await self.estado_provider.limpar_reserva(lto_id)
        
        # 2. Se temos o ID e o provider, restauramos a solicitação na fila
        if sol_id and solicitacao_provider:
            await solicitacao_provider.atualizar(sol_id, {
                "status": "Pendente",
                "destino": None
            })
            
        return {"message": f"Reserva do leito {lto_id} cancelada."}
    
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
        status_vazios = ['DESOCUPADO', 'DISPONIVEL', 'DISPONÍVEL', 'VAGO', 'LIBERADO', 'LIMPEZA', 'VAGO/LIMPO']
        
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
            
            ja_tem_reserva = proximo_paciente is not None and str(proximo_paciente).strip() != ""
            esta_fisicamente_vazio = (prontuario_atual is None or str(prontuario_atual).strip() in ["", "0", "N/D"])
            
            if not ja_tem_reserva:
                if esta_fisicamente_vazio or (status in status_vazios) or (status_local in status_vazios) or tem_alta:
                    disponiveis.append(l)
        
        return disponiveis
