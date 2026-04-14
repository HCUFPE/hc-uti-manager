from fastapi import APIRouter, Depends, HTTPException, status
from typing import List, Dict, Any
from controllers.alerta_controller import AlertaController
from dependencies import get_alerta_controller
from pydantic import BaseModel

router = APIRouter(prefix="/api/alertas", tags=["Alertas"])

class AtualizarLeituraInput(BaseModel):
    lido: bool

@router.get("", response_model=List[Dict[str, Any]])
async def listar_alertas(
    controller: AlertaController = Depends(get_alerta_controller)
):
    """Retorna todos os alertas persistidos no banco de dados."""
    return await controller.listar_alertas()

@router.put("/{alerta_id}/lido")
async def atualizar_status_leitura(
    alerta_id: int,
    payload: AtualizarLeituraInput,
    controller: AlertaController = Depends(get_alerta_controller)
):
    """Atualiza o status de leitura de um alerta."""
    return await controller.atualizar_status_leitura(alerta_id, payload.lido)

@router.post("/gerar", status_code=status.HTTP_201_CREATED)
async def gerar_alertas(
    controller: AlertaController = Depends(get_alerta_controller)
):
    """
    Aciona a rotina de análise do sistema para gerar novos alertas.
    Idealmente chamado por um job agendado, mas exposto para testes.
    """
    return await controller.gerar_alertas()
