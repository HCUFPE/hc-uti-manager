from fastapi import APIRouter, Depends, HTTPException, Query
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

@router.get("/consultar-aghu/{prontuario}", response_model=Dict[str, Any])
async def consultar_aghu(
    prontuario: str,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    current_user: dict = Depends(auth_handler.decode_token),
):
    """Consulta dados de cirurgia agendada no AGHU para o prontuário informado."""
    return await controller.consultar_dados_aghu(prontuario)

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

    username = current_user.get("username", "Sistema")
    await controller.editar_solicitacao(sol_id, payload, user_perfil, username=username)

    # Se houve troca de prontuário, a controller já registrou as ações específicas (cancelamento/criação/reserva) no histórico
    if "prontuario" in payload and str(payload["prontuario"]) != str(solicitacao.prontuario):
        return {"message": "Solicitação editada com sucesso via troca de paciente"}

    prontuario = payload.get("prontuario", "N/D")
    
    # Se mudou a prioridade, usamos um tipo específico para o alerta
    tipo_hist = "edicao"
    if "prioridade" in payload and payload.get("prioridade") != solicitacao.prioridade:
        tipo_hist = "alteracao_prioridade"

    # Tenta pegar a data nova (payload) ou a antiga (solicitacao)
    data_raw = payload.get("data_cirurgia") or solicitacao.data_cirurgia
    data_br = data_raw
    if data_raw and "-" in data_raw:
        p = data_raw.split("-")
        if len(p) == 3: data_br = f"{p[2]}/{p[1]}/{p[0]}"

    await historico.registrar(
        operador=username,
        tipo=tipo_hist,
        acao="Editou solicitação de vaga",
        detalhes=f"Solicitação #{sol_id} (Prontuário {prontuario}) - Data: {data_br}",
        prontuario=str(prontuario)
    )
    return {"message": "Solicitação editada com sucesso"}

@router.delete("/{sol_id}")
async def cancelar_solicitacao(
    sol_id: int,
    motivo: str = Query(None, description="Motivo do cancelamento"),
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
        is_uti = user_perfil in [Role.UTI, Role.UTI_ADMIN]
        is_sol_pendente = solicitacao.status == "Pendente"
        is_motivo_valido = motivo in ["Falta de vaga de UTI", "Paciente já ocupa um leito na UTI"]
        
        if is_uti and is_sol_pendente and is_motivo_valido:
            pass # Permitido para a UTI
        elif solicitacao.perfil_solicitante != user_grupo:
            raise HTTPException(status_code=403, detail="Você não tem permissão para cancelar esta solicitação.")

    await controller.cancelar_solicitacao(sol_id, user_perfil)
    # Formata data para o histórico (BR)
    data_formatada = solicitacao.data_cirurgia
    if data_formatada and "-" in data_formatada:
        p = data_formatada.split("-")
        if len(p) == 3: data_formatada = f"{p[2]}/{p[1]}/{p[0]}"

    detalhes_historico = f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) - Data: {data_formatada}"
    if motivo:
        detalhes_historico += f" - Motivo: {motivo}"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="exclusao_solicitacao",
        acao="Cancelou solicitação de vaga",
        detalhes=detalhes_historico,
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
    motivo: str = Query(..., description="Motivo do cancelamento da reserva"),
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
    
    detalhes_hist = f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) voltou para Pendente"
    if motivo:
        detalhes_hist += f" - Motivo: {motivo}"

    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cancelamento_reserva",
        acao="Cancelou reserva de leito",
        detalhes=detalhes_hist,
        prontuario=str(solicitacao.prontuario)
    )
    return result

@router.post("/{sol_id}/cirurgia-finalizada")
async def marcar_cirurgia_finalizada(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([
        Role.ADMIN, Role.BC, Role.BC_ADMIN, Role.COB, Role.COB_ADMIN, Role.HEM, Role.HEM_ADMIN
    ])),
):
    """Sinaliza que a cirurgia correspondente à solicitação foi concluída."""
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    result = await controller.marcar_cirurgia_finalizada(sol_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="cirurgia_finalizada",
        acao="Cirurgia Finalizada",
        detalhes=f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) com cirurgia concluída.",
        prontuario=str(solicitacao.prontuario)
    )
    return result

@router.post("/{sol_id}/liberar-encaminhamento")
async def liberar_encaminhamento(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    """Autoriza a transferência do paciente para o leito reservado na UTI."""
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    result = await controller.liberar_encaminhamento(sol_id)
    minutos = result.get("minutos_espera")
    duration_str = ""
    if minutos is not None:
        if minutos >= 60:
            horas = minutos // 60
            resto = minutos % 60
            duration_str = f" [Tempo de Liberação: {horas}h {resto}m]"
        else:
            duration_str = f" [Tempo de Liberação: {minutos}m]"
            
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="encaminhamento_liberado",
        acao="Liberou encaminhamento",
        detalhes=f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) - Encaminhamento liberado para {solicitacao.destino or 'UTI'}.{duration_str}",
        prontuario=str(solicitacao.prontuario)
    )
    return result

@router.post("/{sol_id}/cancelar-liberacao")
async def cancelar_liberacao(
    sol_id: int,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    """Revoga a autorização de transferência do paciente para a UTI."""
    solicitacao = await controller.leito_provider.get_por_id(sol_id)
    if not solicitacao:
        raise HTTPException(status_code=404, detail="Solicitação não encontrada")
    
    result = await controller.cancelar_liberacao(sol_id)
    await historico.registrar(
        operador=current_user.get("username", "Sistema"),
        tipo="encaminhamento_cancelado",
        acao="Cancelou liberação de encaminhamento",
        detalhes=f"Solicitação #{sol_id} (Prontuário {solicitacao.prontuario}) - Liberação de encaminhamento cancelada pela UTI.",
        prontuario=str(solicitacao.prontuario)
    )
    return result

@router.post("/{sol_id}/remanejar-reserva")
async def remanejar_reserva(
    sol_id: int,
    payload: dict,
    controller: SolicitacaoLeitoController = Depends(get_solicitacao_leito_controller),
    historico: HistoricoProvider = Depends(get_historico_provider),
    current_user: dict = Depends(check_role([Role.ADMIN, Role.UTI, Role.UTI_ADMIN])),
):
    """Remaneja a reserva de uma solicitação para um novo leito."""
    novo_leito_id = payload.get("leito_id")
    if not novo_leito_id:
        raise HTTPException(status_code=400, detail="O campo 'leito_id' é obrigatório.")
        
    result = await controller.remanejar_reserva(sol_id, novo_leito_id)
    
    prontuario = result.get("prontuario", "?")
    leito_origem = result.get("leito_origem")
    leito_destino = result.get("leito_destino")
    swap_ocorreu = result.get("swap_ocorreu", False)
    
    if swap_ocorreu:
        prontuario_destino = result.get("prontuario_destino", "?")
        # Registrar histórico para o paciente de origem (A)
        await historico.registrar(
            operador=current_user.get("username", "Sistema"),
            tipo="remanejamento_reserva",
            acao="Remanejou reserva (Troca)",
            detalhes=f"Reserva trocada com Prontuário {prontuario_destino}: transferida do Leito {leito_origem} para o Leito {leito_destino}",
            prontuario=str(prontuario)
        )
        # Registrar histórico para o paciente de destino (B)
        await historico.registrar(
            operador=current_user.get("username", "Sistema"),
            tipo="remanejamento_reserva",
            acao="Remanejou reserva (Troca)",
            detalhes=f"Reserva trocada com Prontuário {prontuario}: transferida do Leito {leito_destino} para o Leito {leito_origem}",
            prontuario=str(prontuario_destino)
        )
    else:
        # Sem swap (caso normal)
        await historico.registrar(
            operador=current_user.get("username", "Sistema"),
            tipo="remanejamento_reserva",
            acao="Remanejou reserva de leito",
            detalhes=f"Solicitação #{sol_id} (Prontuário {prontuario}) transferida do Leito {leito_origem} para o Leito {leito_destino}",
            prontuario=str(prontuario)
        )
        
    return result

