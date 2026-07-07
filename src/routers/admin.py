from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

from auth.auth import auth_handler
from auth.roles import Role

router = APIRouter(prefix="/api", tags=["Admin"])

class AdminData(BaseModel):
    message: str
    user_groups: List[str]

async def verify_admin_group(current_user: dict = Depends(auth_handler.decode_token)):
    user_perfil = current_user.get("perfil")
    allowed_admins = [
        Role.ADMIN, Role.UTI_ADMIN, Role.NIR_ADMIN, 
        Role.COB_ADMIN, Role.BC_ADMIN, Role.HEM_ADMIN
    ]
    if user_perfil not in allowed_admins:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores")
    return current_user

@router.get("/admin/ad-search/{username}")
async def buscar_usuario_ad(
    username: str,
    current_user: dict = Depends(verify_admin_group)
):
    """Consulta detalhes de um usuário no Active Directory (AD)."""
    from starlette.concurrency import run_in_threadpool
    try:
        user_info = await run_in_threadpool(
            auth_handler.authenticate_user, 
            username.strip().lower(), 
            None
        )
        
        # Mapear os atributos retornados pelo AD
        display_name = user_info.get("displayName", [""])
        if isinstance(display_name, list) and display_name:
            display_name = display_name[0]
        elif not display_name:
            display_name = user_info.get("cn", [""])[0] if user_info.get("cn") else username
            
        department = user_info.get("department", [""])
        if isinstance(department, list) and department:
            department = department[0]
        elif not department:
            # Fallback para provedor mock
            mock_departments = {
                "admin": "USID / Tecnologia",
                "uti": "Unidade de Terapia Intensiva",
                "nir": "Núcleo Interno de Regulação",
                "cob": "Centro Obstétrico",
                "bloco": "Bloco Cirúrgico",
                "comum": "Enfermarias"
            }
            clean_user = username.strip().lower()
            department = mock_departments.get(clean_user, "Não Informado")
            
        mail = user_info.get("mail", [""])
        if isinstance(mail, list) and mail:
            mail = mail[0]
        elif not mail:
            upn = user_info.get("userPrincipalName", [""])
            if isinstance(upn, list) and upn:
                mail = upn[0]
            else:
                mail = f"{username.strip().lower()}@mock.com"
                
        return {
            "username": username.strip().lower(),
            "nome_completo": display_name,
            "lotacao": department,
            "email": mail
        }
    except Exception as e:
        raise HTTPException(
            status_code=404, 
            detail=f"Usuário '{username}' não localizado no Active Directory."
        )

from models.usuario_perfil import UsuarioPerfil
from resources.database import get_app_db_session
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, delete

@router.get("/admin/perfis")
async def listar_perfis(
    db: AsyncSession = Depends(get_app_db_session),
    current_user: dict = Depends(verify_admin_group)
):
    """Lista todos os usuários com perfil customizado."""
    stmt = select(UsuarioPerfil)
    result = await db.execute(stmt)
    return [p.to_dict() for p in result.scalars().all()]

@router.post("/admin/perfis")
async def salvar_perfil(
    payload: dict,
    db: AsyncSession = Depends(get_app_db_session),
    current_user: dict = Depends(verify_admin_group)
):
    """Atribui um perfil a um usuário (login)."""
    username = payload.get("username").strip().lower()
    perfil = payload.get("perfil")
    
    if not username or perfil not in [r.value for r in Role]:
        raise HTTPException(status_code=400, detail="Username e perfil válido são obrigatórios")

    user_perfil = current_user.get("perfil")

    # Regras para admins de setor
    if user_perfil != Role.ADMIN:
        allowed_profiles = []
        if user_perfil == Role.UTI_ADMIN:
            allowed_profiles = [Role.UTI, Role.COMUM]
        elif user_perfil == Role.NIR_ADMIN:
            allowed_profiles = [Role.NIR, Role.COMUM]
        elif user_perfil == Role.COB_ADMIN:
            allowed_profiles = [Role.COB, Role.COMUM]
        elif user_perfil == Role.BC_ADMIN:
            allowed_profiles = [Role.BC, Role.COMUM]
        elif user_perfil == Role.HEM_ADMIN:
            allowed_profiles = [Role.HEM, Role.COMUM]
            
        if perfil not in allowed_profiles:
            raise HTTPException(status_code=403, detail="Você só pode atribuir usuários ao seu próprio setor.")

    # Verifica se já existe
    stmt = select(UsuarioPerfil).where(UsuarioPerfil.username == username)
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()

    nome_completo = payload.get("nome_completo")
    lotacao = payload.get("lotacao")
    email = payload.get("email")

    if usuario:
        usuario.perfil = perfil
        if nome_completo is not None:
            usuario.nome_completo = nome_completo
        if lotacao is not None:
            usuario.lotacao = lotacao
        if email is not None:
            usuario.email = email
    else:
        novo_usuario = UsuarioPerfil(
            username=username, 
            perfil=perfil,
            nome_completo=nome_completo,
            lotacao=lotacao,
            email=email
        )
        db.add(novo_usuario)
    
    await db.commit()
    return {"message": f"Perfil do usuário {username} atualizado para {perfil}"}

@router.delete("/admin/perfis/{username}")
async def excluir_perfil(
    username: str,
    db: AsyncSession = Depends(get_app_db_session),
    current_user: dict = Depends(verify_admin_group)
):
    """Remove o perfil customizado de um usuário."""
    user_perfil = current_user.get("perfil")
    
    # Verifica perfil atual do alvo para admins setoriais
    if user_perfil != Role.ADMIN:
        stmt_check = select(UsuarioPerfil).where(UsuarioPerfil.username == username.lower())
        result_check = await db.execute(stmt_check)
        alvo = result_check.scalar_one_or_none()
        
        if alvo:
            target_perfil = alvo.perfil
            has_permission = False
            if user_perfil == Role.UTI_ADMIN and target_perfil == Role.UTI:
                has_permission = True
            elif user_perfil == Role.NIR_ADMIN and target_perfil == Role.NIR:
                has_permission = True
            elif user_perfil == Role.COB_ADMIN and target_perfil == Role.COB:
                has_permission = True
            elif user_perfil == Role.BC_ADMIN and target_perfil == Role.BC:
                has_permission = True
            elif user_perfil == Role.HEM_ADMIN and target_perfil == Role.HEM:
                has_permission = True
                
            if not has_permission:
                raise HTTPException(status_code=403, detail="Você não tem permissão para remover perfis fora do seu setor.")

    stmt = delete(UsuarioPerfil).where(UsuarioPerfil.username == username.lower())
    await db.execute(stmt)
    await db.commit()
    return {"message": f"Perfil do usuário {username} removido (agora é Comum)"}
