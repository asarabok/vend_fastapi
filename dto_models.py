
from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel, EmailStr, constr


class OutputMachineModel(BaseModel):
    id: int
    manufacturer: str
    name: str
    model: str


class InputMachineModel(OutputMachineModel):
    id: Optional[int]
    owner_id: int


class BaseUserModel(BaseModel):
    id: Optional[int]
    first_name: constr(min_length=3)
    last_name: constr(min_length=3)
    email: EmailStr


class UserInfoModel(BaseModel):
    user: BaseUserModel
    assigned_machines: List[OutputMachineModel] = []


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
    product_category_id: Optional[int]


class OutputProductListModel(BaseModel):
    id: int
    title: constr(max_length=50)
    created_at: datetime
    product_category: Optional[OutputSingleProductCategoryModel]


class OutputSingleProductModel(OutputProductListModel):
    created_by: int
    updated_by: Optional[int] = None
    updated_at: Optional[datetime] = None
