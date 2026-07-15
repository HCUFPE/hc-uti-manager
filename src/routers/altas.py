from fastapi import APIRouter, Depends, HTTPException
from auth.roles import Role
from typing import List, Dict, Any
from controllers.altas_controller import AltasController
from dependencies import get_altas_controller, get_historico_provider, check_role
from providers.implementations.historico_provider import HistoricoProvider
from auth.auth import auth_handler

router = APIRouter(prefix="/api/altas", tags=["Altas"])


@router.get("", response_model=List[Dict[str, Any]])
async def listar_altas(
    controller: AltasController = Depends(get_altas_controller)
):
    """Retorna todas as solicitações de alta pendentes/definidas,
    enriquecidas com dados do paciente do AGHU."""
    return await controller.listar_altas()


@router.post("/{lto_id}")
async def solicitar_alta(
    lto_id: str,
    payload: dict = {},
    controller: AltasController = Depends(get_altas_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    """Registra uma nova solicitação de alta para o leito especificado."""
    result = await controller.solicitar_alta(lto_id, payload)
    
    # Obtém o prontuário do ocupante atual para o histórico
    leitos_censo = await controller.leitos_controller.listar_leitos()
    leito_info = next((l for l in leitos_censo if l['lto_lto_id'] == lto_id), None)
    prontuario = str(leito_info['prontuario_atual']) if leito_info and leito_info.get('prontuario_atual') else "N/D"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="alta",
        acao="Solicitou alta",
        detalhes=f"Leito {lto_id}",
        prontuario=prontuario,
    )
    return result


@router.put("/{alta_id}")
async def atualizar_destino(
    alta_id: int,
    payload: dict,
    controller: AltasController = Depends(get_altas_controller),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.NIR, Role.NIR_ADMIN])),
):
    """Atualiza o destino e/ou necessidades especiais de uma solicitação de alta."""
    return await controller.atualizar_destino(alta_id, payload, operador=current_user.get("username", "NIR"))

@router.patch("/{alta_id}/disponivel")
async def marcar_destino_disponivel(
    alta_id: int,
    payload: dict,
    controller: AltasController = Depends(get_altas_controller),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.NIR, Role.NIR_ADMIN]))
):
    """NIR confirma que o destino já está disponível (leito vago e pronto)."""
    disponivel = payload.get("disponivel", True)
    return await controller.atualizar_destino_disponivel(alta_id, disponivel, operador=current_user.get("username", "NIR"))


@router.delete("/{alta_id}", status_code=204)
async def cancelar_alta(
    alta_id: int,
    motivo: str = None,
    controller: AltasController = Depends(get_altas_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN, Role.NIR, Role.NIR_ADMIN])),
):
    """Cancela uma solicitação de alta."""
    alvo = await controller.alta_provider.get_por_id(alta_id)
    prontuario = alvo.prontuario if alvo else "Desconhecido"
    
    await controller.cancelar_alta(alta_id)
    
    perfil = current_user.get("perfil")
    is_nir = perfil in [Role.NIR, Role.NIR_ADMIN]
    
    detalhes_hist = f"Alta #{alta_id} (Prontuário {prontuario})"
    if is_nir:
        detalhes_hist += " cancelada pelo NIR"
    else:
        detalhes_hist += " cancelada"
        
    if motivo:
        detalhes_hist += f". Motivo: {motivo}"
        
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento",
        acao="Cancelou solicitação de alta",
        detalhes=detalhes_hist,
        prontuario=str(prontuario)
    )
