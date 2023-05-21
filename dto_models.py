
from datetime import datetime
from typing import List, Optional

from pydantic import (
    BaseModel,
    EmailStr,
    conint,
    conlist,
    constr,
)


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


class InputCreateProductCategoryModel(BaseModel):
    title: constr(max_length=50)


class InputUpdateProductCategoryModel(InputCreateProductCategoryModel):
    pass


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


class OutputMachineColumnModel(BaseModel):
    index: conint(ge=0, le=20)
    current_quantity: conint(ge=0, le=20)
    spiral_quantity: conint(ge=0, le=20)
    price: float
    product: OutputSingleProductModel


class OutputMachineListModel(OutputMachineModel):
    owner: BaseUserModel
    columns: List[OutputMachineColumnModel] = []


class InputAddMachineColumn(BaseModel):
    product_id: int
    price: float


class InputMachinePlanogramChangeModel(BaseModel):
    columns: conlist(InputAddMachineColumn, min_items=1, max_items=20)
