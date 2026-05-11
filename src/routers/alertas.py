from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from controllers.alerta_controller import AlertaController
from dependencies import get_alerta_controller
from auth.auth import auth_handler
from pydantic import BaseModel

router = APIRouter(prefix="/api/alertas", tags=["Alertas"])

class AtualizarLeituraInput(BaseModel):
    lido: bool

@router.get("", response_model=List[Dict[str, Any]])
async def listar_alertas(
    controller: AlertaController = Depends(get_alerta_controller),
    current_user: dict = Depends(auth_handler.decode_token)
):
    """Retorna todos os alertas persistidos, filtrados pelo perfil do usuário."""
    perfil = current_user.get("perfil", "Comum")
    return await controller.listar_alertas(perfil)

@router.get("/unread-count")
async def get_unread_count(
    controller: AlertaController = Depends(get_alerta_controller),
    current_user: dict = Depends(auth_handler.decode_token)
):
    perfil = current_user.get("perfil", "Comum")
    alertas = await controller.listar_alertas(perfil)
    count = len([a for a in alertas if not a.get("lido")])
    return {"count": count}

@router.put("/{alerta_id}/lido")
async def atualizar_status_leitura(
    alerta_id: int,
    payload: AtualizarLeituraInput,
    controller: AlertaController = Depends(get_alerta_controller)
):
    """Atualiza o status de leitura de um alerta."""
    return await controller.atualizar_status_leitura(alerta_id, payload.lido)

@router.put("/lidos")
async def marcar_todos_como_lidos(
    controller: AlertaController = Depends(get_alerta_controller),
    current_user: dict = Depends(auth_handler.decode_token)
):
    """Marca todos os alertas visíveis para o usuário como lidos."""
    perfil = current_user.get("perfil", "Comum")
    return await controller.marcar_todos_como_lidos(perfil)

@router.post("/gerar", status_code=status.HTTP_201_CREATED)
async def gerar_alertas(
    controller: AlertaController = Depends(get_alerta_controller)
):
    """
    Aciona a rotina de análise do sistema para gerar novos alertas.
    Idealmente chamado por um job agendado, mas exposto para testes.
    """
    return await controller.gerar_alertas()
