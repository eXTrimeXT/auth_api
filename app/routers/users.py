from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from .. import schemas, models, auth, database
from ..dependencies import get_current_active_user

router = APIRouter(prefix="/users", tags=["users"])

@router.get("/me", response_model=schemas.UserResponse)
def get_current_user_info(current_user: models.User = Depends(get_current_active_user)):
    return current_user

@router.put("/me", response_model=schemas.UserResponse)
def update_current_user(
        user_update: schemas.UserUpdate,
        current_user: models.User = Depends(get_current_active_user),
        db: Session = Depends(database.get_db)
):
    if user_update.email and user_update.email != current_user.email:
        existing_user = db.query(models.User).filter(models.User.email == user_update.email).first()
        if existing_user:
            raise HTTPException(status_code=400, detail="Email already registered")
        current_user.email = user_update.email

    if user_update.first_name:
        current_user.first_name = user_update.first_name
    if user_update.last_name:
        current_user.last_name = user_update.last_name
    if user_update.middle_name is not None:
        current_user.middle_name = user_update.middle_name

    db.commit()
    db.refresh(current_user)
    return current_user

@router.delete("/me", status_code=status.HTTP_204_NO_CONTENT)
def delete_current_user(
        current_user: models.User = Depends(get_current_active_user),
        db: Session = Depends(database.get_db)
):
    current_user.is_active = False
    db.commit()
    return None