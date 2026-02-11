from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..dependencies import require_admin

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/roles", response_model=schemas.RoleResponse, status_code=status.HTTP_201_CREATED)
def create_role(
        role: schemas.RoleCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    existing_role = db.query(models.Role).filter(models.Role.name == role.name).first()
    if existing_role:
        raise HTTPException(status_code=400, detail="Role already exists")

    db_role = models.Role(**role.dict())
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

@router.get("/roles", response_model=List[schemas.RoleResponse])
def get_roles(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    roles = db.query(models.Role).all()
    return roles

@router.post("/business-elements", response_model=schemas.BusinessElementResponse, status_code=status.HTTP_201_CREATED)
def create_business_element(
        element: schemas.BusinessElementCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    existing_element = db.query(models.BusinessElement).filter(
        models.BusinessElement.name == element.name
    ).first()
    if existing_element:
        raise HTTPException(status_code=400, detail="Business element already exists")

    db_element = models.BusinessElement(**element.dict())
    db.add(db_element)
    db.commit()
    db.refresh(db_element)
    return db_element

@router.post("/access-rules", response_model=schemas.AccessRuleResponse, status_code=status.HTTP_201_CREATED)
def create_access_rule(
        rule: schemas.AccessRuleCreate,
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    db_rule = models.AccessRoleRule(**rule.dict())
    db.add(db_rule)
    db.commit()
    db.refresh(db_rule)
    return db_rule

@router.get("/access-rules", response_model=List[schemas.AccessRuleResponse])
def get_access_rules(
        db: Session = Depends(database.get_db),
        current_user: models.User = Depends(require_admin)
):
    rules = db.query(models.AccessRoleRule).all()
    return rules