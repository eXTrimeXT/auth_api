from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session
from . import models, database, auth
from typing import List

def get_current_active_user(current_user: models.User = Depends(auth.get_current_user)):
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

def check_permission(db: Session, user: models.User, element_name: str, permission_type: str):
    element = db.query(models.BusinessElement).filter(
        models.BusinessElement.name == element_name
    ).first()

    if not element:
        return False

    rule = db.query(models.AccessRoleRule).filter(
        models.AccessRoleRule.role_id == user.role_id,
        models.AccessRoleRule.business_element_id == element.id
    ).first()

    if not rule:
        return False

    permission_attr = f"{permission_type}_permission"
    return getattr(rule, permission_attr, False)

def require_permission(element_name: str, permission_type: str):
    async def permission_checker(
            current_user: models.User = Depends(auth.get_current_user),
            db: Session = Depends(database.get_db)
    ):
        has_permission = check_permission(db, current_user, element_name, permission_type)
        if not has_permission:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Not enough permissions"
            )
        return current_user
    return permission_checker

def require_admin(db: Session = Depends(database.get_db), current_user: models.User = Depends(auth.get_current_user)):
    admin_role = db.query(models.Role).filter(models.Role.name == "admin").first()
    if not admin_role or current_user.role_id != admin_role.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin privileges required"
        )
    return current_user