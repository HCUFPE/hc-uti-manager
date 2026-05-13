from fastapi import APIRouter, Depends, HTTPException
from auth.roles import Role
from typing import List, Dict, Any
from controllers.solicitacao_leito_controller import SolicitacaoLeitoController
from dependencies import get_solicitacao_leito_controller, get_historico_provider, get_app_db_session, check_role
from providers.implementations.historico_provider import HistoricoProvider
from models.usuario_perfil import UsuarioPerfil
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from auth.auth import auth_handler

router = APIRouter(prefix="/api/solicitacoes", tags=["Solicitacoes"])

@router.get("", response_model=List[Dict[str, Any]])
async def listar_solicitacoes(
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller)
):
    """Retorna todas as solicitações de leito ativas."""
    return await controller.listar_solicitacoes()

@router.post("")
async def criar_solicitacao(
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([
        Role.ADMIN, Role.COB, Role.COB_ADMIN, Role.BC, Role.BC_ADMIN, Role.HEM, Role.HEM_ADMIN
    ])),
):
    """Cria uma nova solicitação de leito."""
    user_perfil = current_user.get("perfil", "Comum")
    # Remove o sufixo -Admin para gravar apenas o grupo base
    grupo_solicitante = user_perfil.replace("-Admin", "")
    payload["perfil_solicitante"] = grupo_solicitante
    
    # Primeiro cria a solicitação
    result = await controller.criar_solicitacao(payload)
    
    # Busca a solicitação recém criada para pegar o ID real
    sols = await controller.leito_provider.get_todas()
    nova_vaga = next((s for s in sols if str(s.prontuario) == str(payload.get("prontuario"))), None)
    sol_id = nova_vaga.id if nova_vaga else "?"

    prontuario = payload.get("prontuario", "")
    especialidade = payload.get("especialidade", "")
    tipo_sol = payload.get("tipo", "")
    
    data_original = payload.get("data_cirurgia", "")
    data_br = data_original
    if data_original and "-" in data_original:
        p = data_original.split("-")
        if len(p) == 3: data_br = f"{p[2]}/{p[1]}/{p[0]}"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="nova_solicitacao",
        acao="Nova solicitação de vaga",
        detalhes=f"Solicitação #{sol_id} - Prontuário {prontuario} — {especialidade} ({tipo_sol}) - Data: {data_br}",
        prontuario=str(prontuario)
    )
    return result

@router.put("/{sol_id}")
async def atualizar_status(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    """Atualiza o status ou o destino de uma solicitação."""

    result = await controller.atualizar_status(sol_id, payload)
    novo_status = payload.get("status", "")
    destino = payload.get("destino", "")
    detalhe = f"Solicitação #{sol_id}"
    if destino:
        detalhe += f" → {destino}"
    # Tenta pegar o prontuário da solicitação para o histórico
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    prontuario = solicitacao.prontuario if solicitacao else None

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="destino" if destino else "status",
        acao=f"Atualizou status para {novo_status}" if novo_status else "Definiu destino",
        detalhes=detalhe,
        prontuario=str(prontuario) if prontuario else None
    )
    return result

@router.patch("/{sol_id}")
async def editar_solicitacao(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Atualiza dados de uma solicitação (apenas para UTI/NIR ou o próprio dono)."""
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    # Identifica o perfil (token)
    user_perfil = current_user.get("perfil", "Comum")
    user_grupo = user_perfil.replace("-Admin", "")
    
    if user_perfil != Role.ADMIN:
        if solicitacao.perfil_solicitante != user_grupo:
            raise HTTPException(status_code=403, detail="Você não tem permissão para editar esta solicitação.")

    await controller.editar_solicitacao(sol_id, payload)
    prontuario = payload.get("prontuario", "N/D")
    
    # Se mudou a prioridade, usamos um tipo específico para o alerta
    tipo_hist = "edicao"
    if "prioridade" in payload:
        tipo_hist = "alteracao_prioridade"

    # Tenta pegar a data nova (payload) ou a antiga (solicitacao)
    data_raw = payload.get("data_cirurgia") or solicitacao.data_cirurgia
    data_br = data_raw
    if data_raw and "-" in data_raw:
        p = data_raw.split("-")
        if len(p) == 3: data_br = f"{p[2]}/{p[1]}/{p[0]}"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo=tipo_hist,
        acao="Editou solicitação de vaga",
        detalhes=f"Solicitação #{sol_id} (Prontuário {prontuario}) - Data: {data_br}",
        prontuario=str(prontuario)
    )
    return {"message": "Solicitação editada com sucesso"}

@router.delete("/{sol_id}")
async def cancelar_solicitacao(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Cancela uma solicitação de leito."""
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    user_perfil = current_user.get("perfil", "Comum")
    user_grupo = user_perfil.replace("-Admin", "")
    
    if user_perfil != Role.ADMIN:
        if solicitacao.perfil_solicitante != user_grupo:
            raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar esta solicitação.")

    await controller.cancelar_solicitacao(sol_id)
    # Formata data para o histórico (BR)
    data_formatada = solicitacao.data_cirurgia
    if data_formatada and "-" in data_formatada:
        p = data_formatada.split("-")
        if len(p) == 3: data_formatada = f"{p[2]}/{p[1]}/{p[0]}"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="exclusao_solicitacao",
        acao="Cancelou solicitação de vaga",
        detalhes=f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) - Data: {data_formatada}",
        prontuario=str(solicitacao.prontuario)
    )
    return {"message": "Solicitação cancelada com sucesso"}

@router.post("/{sol_id}/reservar")
async def reservar_leito(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    """Reserva um leito para uma solicitação pendente."""
        
    leito_id = payload.get("leito_id")
    result = await controller.reservar_leito(sol_id, leito_id)
    # Busca a solicitação para pegar o prontuário
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    prontuario = solicitacao.prontuario if solicitacao else "?"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="reserva",
        acao="Reservou leito para solicitação",
        detalhes=f"Solicitação #{sol_id} (Prontuário {prontuario}) para Leito {leito_id}",
        prontuario=str(prontuario)
    )
    return result

@router.post("/{sol_id}/cancelar-reserva")
async def cancelar_reserva(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Cancela a reserva de um leito, voltando a solicitação para Pendente."""
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")

    user_perfil = current_user.get("perfil", "Comum")
    user_grupo = user_perfil.replace("-Admin", "")
    super_usuarios = [Role.ADMIN, Role.UTI, Role.UTI_ADMIN]
    
    if user_perfil not in super_usuarios:
        if solicitacao.perfil_solicitante != user_grupo:
            raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar a reserva deste paciente.")

    result = await controller.cancelar_reserva(sol_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento_reserva",
        acao="Cancelou reserva de leito",
        detalhes=f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) voltou para Pendente",
        prontuario=str(solicitacao.prontuario)
    )
    return result
