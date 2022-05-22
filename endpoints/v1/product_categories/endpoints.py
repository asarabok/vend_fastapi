from database import session
from db_models import ProductCategory
from dependencies import verify_authorization_token
from dto_models import (
    InputProductCategoryModel,
    OutputSingleProductCategoryModel
)
from fastapi import APIRouter, Body, Depends, HTTPException, status
from mappers import (
    map_to_output_list_product_category_model,
    map_to_output_single_product_category_model
)
from pagination import (
    PaginatedMetaModel,
    PaginatedResponseModel,
    Pagination,
    PaginationInputModel
)
from sqlalchemy.exc import IntegrityError

product_categories_router = APIRouter(
    prefix="/product-categories", tags=["Product Category"])


@product_categories_router.get(
    "",
    response_model=PaginatedResponseModel,
    summary="Get paginated product categories"
)
async def get_product_categories(
    pagination: PaginationInputModel = Depends(),
    decoded_token: dict = Depends(verify_authorization_token)
):
    product_categories_query = session.query(
        ProductCategory
    ).order_by(
        ProductCategory.title.asc()
    )

    product_categories = Pagination.paginate_query(
        product_categories_query, pagination.page, pagination.page_size)
    total_items, num_pages = Pagination.get_total_items_and_pages(
        product_categories_query, pagination.page_size)

    output_product_categories = [
        map_to_output_list_product_category_model(p)
        for p in product_categories
    ]

    output_meta = PaginatedMetaModel(
        page=pagination.page,
        page_size=pagination.page_size,
        num_pages=num_pages,
        total_items=total_items
    )
    return PaginatedResponseModel(
        meta=output_meta, content=output_product_categories)


@product_categories_router.post(
    "",
    response_model=OutputSingleProductCategoryModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create product category"
)
async def create_product_category(
    decoded_token: dict = Depends(verify_authorization_token),
    product_category_model: InputProductCategoryModel = Body()
):
    product_category_model.created_by = decoded_token["id"]
    product_category = ProductCategory(**product_category_model.dict())

    session.add(product_category)

    try:
        session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Product category with title {product_category_model.title} "
                "already exists!"
            )
        )

    return map_to_output_single_product_category_model(product_category)
