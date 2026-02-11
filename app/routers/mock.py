from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, models, database
from ..dependencies import require_permission, get_current_active_user, check_permission

router = APIRouter(prefix="/mock", tags=["mock-business"])

# Mock data storage
mock_products = []
mock_orders = []

@router.get("/products", response_model=List[schemas.MockProduct])
def get_products(
        current_user: models.User = Depends(require_permission("products", "read")),
        db: Session = Depends(database.get_db)
):
    return mock_products

@router.post("/products", response_model=schemas.MockProduct, status_code=status.HTTP_201_CREATED)
def create_product(
        product: schemas.MockProduct,
        current_user: models.User = Depends(require_permission("products", "create")),
        db: Session = Depends(database.get_db)
):
    product.owner_id = current_user.id
    mock_products.append(product)
    return product

@router.put("/products/{product_id}", response_model=schemas.MockProduct)
def update_product(
        product_id: int,
        product_update: schemas.MockProduct,
        current_user: models.User = Depends(require_permission("products", "update")),
        db: Session = Depends(database.get_db)
):
    for i, product in enumerate(mock_products):
        if product.id == product_id:
            if product.owner_id == current_user.id or check_permission(db, current_user, "products", "update_all"):
                mock_products[i] = product_update
                return product_update
            raise HTTPException(status_code=403, detail="Not enough permissions")
    raise HTTPException(status_code=404, detail="Product not found")

@router.delete("/products/{product_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_product(
        product_id: int,
        current_user: models.User = Depends(require_permission("products", "delete")),
        db: Session = Depends(database.get_db)
):
    for i, product in enumerate(mock_products):
        if product.id == product_id:
            if product.owner_id == current_user.id or check_permission(db, current_user, "products", "delete_all"):
                mock_products.pop(i)
                return None
            raise HTTPException(status_code=403, detail="Not enough permissions")
    raise HTTPException(status_code=404, detail="Product not found")

@router.get("/orders", response_model=List[schemas.MockOrder])
def get_orders(
        current_user: models.User = Depends(require_permission("orders", "read")),
        db: Session = Depends(database.get_db)
):
    return mock_orders

@router.post("/orders", response_model=schemas.MockOrder, status_code=status.HTTP_201_CREATED)
def create_order(
        order: schemas.MockOrder,
        current_user: models.User = Depends(require_permission("orders", "create")),
        db: Session = Depends(database.get_db)
):
    order.user_id = current_user.id
    mock_orders.append(order)
    return order