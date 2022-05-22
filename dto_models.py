import os

from typing import Any, List, Optional

from pydantic import BaseModel, EmailStr, conint, constr


class PaginationInputModel(BaseModel):
    page: conint(gt=0) = 1
    page_size: conint(gt=0, lt=51) = int(os.environ['PAGE_SIZE'])


class PaginatedMetaModel(BaseModel):
    page: conint(gt=0)
    page_size: conint(gt=0, lt=51)
    num_pages: int
    total_items: int


class PaginatedResponseModel(BaseModel):
    meta: PaginatedMetaModel
    content: List[Any]


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


class BaseProductCategoryModel(BaseModel):
    title: constr(max_length=50)
    created_by: Optional[int]


class OutputProductCategoryModel(BaseModel):
    id: int
    title: constr(max_length=50)


"""
# Product
class BaseProductModel(BaseModel):
    title: str


class InputProductModel(BaseProductModel):
    pass


class OutputProductModel(BaseProductModel):
    id: int

# Machine


# Machine Column

class MachineColumn(BaseModel):
    id: conint(gt=0)
    index: conint(gt=1000, lt=1024)
    current_quantity: int
    spiral_quantity: int
    price = float


class Machine(BaseModel):
    id: int
    manufacturer: str
    name: str
    model: str
    columns = List[MachineColumn]
"""
