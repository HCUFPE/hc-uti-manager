from fastapi import APIRouter, Depends, HTTPException, status
from pydantic import BaseModel
from typing import List

from auth.auth import auth_handler
from auth.roles import Role, get_user_role

router = APIRouter(prefix="/api", tags=["Admin"])

class AdminData(BaseModel):
    message: str
    user_groups: List[str]

async def verify_admin_group(current_user: dict = Depends(auth_handler.decode_token)):
    user_role = get_user_role(current_user.get("groups", []))
    if user_role != Role.ADMIN:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not enough privileges")
    return current_user

@router.get("/admin-only-data", response_model=AdminData)
async def get_admin_data(current_user: dict = Depends(verify_admin_group)):
    """
    Returns data only accessible by users with admin privileges.
    """
    return AdminData(
        message="This is highly confidential admin data!",
        user_groups=current_user.get("groups", [])
    )
