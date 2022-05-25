from db_models import Product
from dependencies import get_db, verify_authorization_token
from dto_models import InputProductModel, OutputSingleProductModel
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pagination import (
    PaginatedMetaModel,
    PaginatedResponseModel,
    Pagination,
    PaginationInputModel
)
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session, joinedload

from endpoints.v1.products.mappers import (
    map_to_output_product_list_model,
    map_to_output_single_product_model
)

products_router = APIRouter(
    prefix="/products", tags=["Product"])


@products_router.get(
    "",
    response_model=PaginatedResponseModel,
    summary="Get paginated products"
)
def get_products(
    session: Session = Depends(get_db),
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
    session: Session = Depends(get_db),
    decoded_token: dict = Depends(verify_authorization_token),
    product_model: InputProductModel = Body()
):
    product = Product(**product_model.dict(), created_by=decoded_token["id"])

    session.rollback()
    session.add(product)

    try:
        session.commit()

    except IntegrityError:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=(
                f"Product with title {product.title} "
                f"and category ID {product.product_category_id} cannot be added!"
            )
        )

    return map_to_output_single_product_model(product)


@products_router.get(
    "/{item_id}",
    response_model=OutputSingleProductModel,
    summary="Get single product"
)
def get_single_product(
    session: Session = Depends(get_db),
    decoded_token: dict = Depends(verify_authorization_token),
    item_id: int = Path(title="Product ID")
):
    product = session.query(
        Product
    ).filter(
        Product.id == item_id
    ).one_or_none()

    if not product:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Product with ID {item_id} not found!"
            )
        )

    return map_to_output_single_product_model(product)
