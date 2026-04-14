from models.reserva_leito import ReservaLeitoInput
from typing import List, Dict, Any, Optional
from datetime import date, datetime

class LeitosController:
    def __init__(self, census_provider, estado_provider, alta_provider=None):
        """
        census_provider: AGHU (PostgreSQL) — dados em tempo real do hospital.
        estado_provider: Sempre o banco local (SQLite) - Reservas.
        alta_provider: Banco local (SQLite) - Solicitações de Alta.
        """
        self.census_provider = census_provider
        self.estado_provider = estado_provider
        self.alta_provider = alta_provider

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
        leitos = await self.census_provider.listar_leitos()
        
        # 2. Busca estados locais (Reservas)
        estados = await self.estado_provider.obter_estados()
        
        # 3. Busca solicitações de alta (Novas)
        altas_map = {}
        if self.alta_provider:
            altas_map = await self.alta_provider.obter_altas_map()
        
        # 4. Merge
        for leito in leitos:
            lto_id = leito.get('lto_lto_id')
            
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

            # Reservas
            if lto_id in estados:
                est = estados[lto_id]
                leito['prontuario_proximo'] = est.prontuario_proximo
                leito['idade_proximo'] = est.idade_proximo
                leito['especialidade_proximo'] = est.especialidade_proximo
            else:
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
        return [
            l for l in leitos 
            if l.get('alta_solicitada') and not l.get('prontuario_proximo')
        ]
