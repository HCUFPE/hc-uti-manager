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
    if user_perfil != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Acesso restrito a administradores")
    return current_user

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
    
    if not username or not perfil:
        raise HTTPException(status_code=400, detail="Username e perfil são obrigatórios")

    # Verifica se já existe
    stmt = select(UsuarioPerfil).where(UsuarioPerfil.username == username)
    result = await db.execute(stmt)
    usuario = result.scalar_one_or_none()

    if usuario:
        usuario.perfil = perfil
    else:
        novo_usuario = UsuarioPerfil(username=username, perfil=perfil)
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
    stmt = delete(UsuarioPerfil).where(UsuarioPerfil.username == username.lower())
    await db.execute(stmt)
    await db.commit()
    return {"message": f"Perfil do usuário {username} removido (agora é Comum)"}
