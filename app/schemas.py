from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# User
class UserBase(BaseModel):
    email: EmailStr
    first_name: str
    last_name: str
    middle_name: Optional[str] = None

class UserCreate(UserBase):
    password: str
    password_confirm: str

class UserUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    middle_name: Optional[str] = None
    email: Optional[EmailStr] = None

class UserResponse(UserBase):
    id: int
    is_active: bool
    role_id: int
    created_at: datetime

    class Config:
        from_attributes = True

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

# Role
class RoleBase(BaseModel):
    name: str
    description: Optional[str] = None

class RoleCreate(RoleBase):
    pass

class RoleResponse(RoleBase):
    id: int

    class Config:
        from_attributes = True

# для работы с токенами
class TokenData(BaseModel):
    user_id: Optional[str] = None

# Business
class BusinessElementBase(BaseModel):
    name: str
    description: Optional[str] = None

class BusinessElementCreate(BusinessElementBase):
    pass

class BusinessElementResponse(BusinessElementBase):
    id: int

    class Config:
        from_attributes = True

# Access Rule
class AccessRuleBase(BaseModel):
    role_id: int
    business_element_id: int
    read_permission: bool = False
    read_all_permission: bool = False
    create_permission: bool = False
    update_permission: bool = False
    update_all_permission: bool = False
    delete_permission: bool = False
    delete_all_permission: bool = False

class AccessRuleCreate(AccessRuleBase):
    pass

class AccessRuleResponse(AccessRuleBase):
    id: int

    class Config:
        from_attributes = True

# Mocks
class MockProduct(BaseModel):
    id: int
    name: str
    owner_id: int

class MockOrder(BaseModel):
    id: int
    product_id: int
    user_id: int