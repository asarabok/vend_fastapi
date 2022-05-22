
from database import session
from db_models import Product
from dependencies import verify_authorization_token

from fastapi import APIRouter, Body, Depends, HTTPException, status
from dto_models import InputProductModel, OutputSingleProductModel
from endpoints.v1.products.mappers import map_to_output_product_list_model, map_to_output_single_product_model
from pagination import (
    PaginatedMetaModel,
    PaginatedResponseModel,
    Pagination,
    PaginationInputModel
)

from sqlalchemy.orm import joinedload
from sqlalchemy.exc import IntegrityError

products_router = APIRouter(
    prefix="/products", tags=["Products"])


@products_router.get(
    "",
    response_model=PaginatedResponseModel,
    summary="Get paginated products"
)
def get_products(
    pagination: PaginationInputModel = Depends(),
    decoded_token: dict = Depends(verify_authorization_token)
):
    products_query = session.query(
        Product
    ).options(
        joinedload(Product.product_category)
    ).order_by(
        Product.title.asc()
    )

    products = Pagination.paginate_query(
        products_query, pagination.page, pagination.page_size)
    total_items, num_pages = Pagination.get_total_items_and_pages(
        products_query, pagination.page_size)

    output_product_categories = [
        map_to_output_product_list_model(p)
        for p in products
    ]

    output_meta = PaginatedMetaModel(
        page=pagination.page,
        page_size=pagination.page_size,
        num_pages=num_pages,
        total_items=total_items
    )
    return PaginatedResponseModel(
        meta=output_meta, content=output_product_categories)


@products_router.post(
    "",
    response_model=OutputSingleProductModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create product"
)
def create_product(
    decoded_token: dict = Depends(verify_authorization_token),
    product_model: InputProductModel = Body()
):
    product_model.created_by = decoded_token["id"]
    product = Product(**product_model.dict())

    session.add(product)

    try:
        session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Product with title {product.title} "
                "already exists!"
            )
        )

    return map_to_output_single_product_model(product)
