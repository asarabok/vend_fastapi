from datetime import datetime

from database import session
from db_models import Machine, MachineColumn, Product, ProductCategory
from dependencies import verify_authorization_token
from dto_models import (
    InputProductCategoryModel,
    OutputSingleProductCategoryModel
)
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pagination import (
    PaginatedMetaModel,
    PaginatedResponseModel,
    Pagination,
    PaginationInputModel
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import joinedload

from endpoints.v1.machines.mappers import map_to_output_single_machine_model

machines_router = APIRouter(
    prefix="/machines", tags=["Machine"])


@machines_router.get(
    "",
    response_model=PaginatedResponseModel,
    summary="Get paginated machines"
)
def get_machines(
    pagination: PaginationInputModel = Depends(),
    decoded_token: dict = Depends(verify_authorization_token)
):
    machines_query = session.query(
        Machine
    ).options(
        joinedload(Machine.owner)
    ).options(
        joinedload(
            Machine.columns
            ).joinedload(
                MachineColumn.product
                ).joinedload(
                    Product.product_category
                )
    ).order_by(
        Machine.id.desc()
    )

    machines = Pagination.paginate_query(
        machines_query, pagination.page, pagination.page_size)
    total_items, num_pages = Pagination.get_total_items_and_pages(
        machines_query, pagination.page_size)

    output_machines = [
        map_to_output_single_machine_model(m)
        for m in machines
    ]

    output_meta = PaginatedMetaModel(
        page=pagination.page,
        page_size=pagination.page_size,
        num_pages=num_pages,
        total_items=total_items
    )
    return PaginatedResponseModel(
        meta=output_meta, content=output_machines)
