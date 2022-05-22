
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, EmailStr, constr


class BaseUserModel(BaseModel):
    id: Optional[int]
    first_name: constr(min_length=3)
    last_name: constr(min_length=3)
    email: EmailStr


class LoginUserModel(BaseModel):
    email: EmailStr
    password: constr(min_length=8)


class CreateUserModel(BaseUserModel, LoginUserModel):
    email: EmailStr
    password: constr(min_length=8)


class AuthenticatedUserResponseModel(BaseModel):
    token: str


class InputProductCategoryModel(BaseModel):
    title: constr(max_length=50)
    created_by: Optional[int]


class OutputListProductCategoryModel(BaseModel):
    id: int
    title: constr(max_length=50)
    created_at: datetime


class OutputSingleProductCategoryModel(OutputListProductCategoryModel):
    created_by: int
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None


class InputProductModel(BaseModel):
    title: constr(max_length=50)
    created_by: Optional[int]
    product_category: Optional[OutputSingleProductCategoryModel]


class OutputProductListModel(BaseModel):
    id: int
    title: constr(max_length=50)
    created_at: datetime
    product_category: Optional[OutputSingleProductCategoryModel]


class OutputSingleProductModel(OutputProductListModel):
    created_by: int
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None
