from datetime import datetime

from database import session
from db_models import ProductCategory
from dependencies import verify_authorization_token
from dto_models import (
    InputCreateProductCategoryModel,
    InputUpdateProductCategoryModel,
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

from endpoints.v1.product_categories.mappers import (
    map_to_output_product_category_list_model,
    map_to_output_single_product_category_model
)

product_categories_router = APIRouter(
    prefix="/product-categories", tags=["Product Category"])


@product_categories_router.get(
    "",
    response_model=PaginatedResponseModel,
    summary="Get paginated product categories"
)
def get_product_categories(
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
        map_to_output_product_category_list_model(p)
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


@product_categories_router.get(
    "/{item_id}",
    response_model=OutputSingleProductCategoryModel,
    summary="Get single product category"
)
def get_single_product_category(
    decoded_token: dict = Depends(verify_authorization_token),
    item_id: int = Path(title="Product category ID")
):
    product_category = session.query(
        ProductCategory
    ).filter(
        ProductCategory.id == item_id
    ).one_or_none()

    if not product_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Product category with ID {item_id} not found!"
            )
        )

    return map_to_output_single_product_category_model(product_category)


@product_categories_router.delete(
    "/{item_id}",
    response_model=dict,
    summary="Delete single product category"
)
def delete_single_product_category(
    decoded_token: dict = Depends(verify_authorization_token),
    item_id: int = Path(title="Product category ID")
):
    product_category = session.query(
        ProductCategory
    ).filter(
        ProductCategory.id == item_id
    ).one_or_none()

    if not product_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Product category with ID {item_id} not found!"
            )
        )

    session.delete(product_category)
    session.commit()

    return {
        "message": f"Product category with ID {item_id} successfully deleted!"
    }


@product_categories_router.patch(
    "/{item_id}",
    response_model=OutputSingleProductCategoryModel,
    summary="Update single product category"
)
def update_single_product_category(
    decoded_token: dict = Depends(verify_authorization_token),
    item_id: int = Path(title="Product category ID"),
    product_category_model: InputUpdateProductCategoryModel = Body()
):
    product_category = session.query(
        ProductCategory
    ).filter(
        ProductCategory.id == item_id
    ).one_or_none()

    if not product_category:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=(
                f"Product category with ID {item_id} not found!"
            )
        )

    product_category.title = product_category_model.title
    product_category.updated_at = datetime.now()
    product_category.updated_by = decoded_token["id"]

    session.add(product_category)
    session.commit()

    return map_to_output_single_product_category_model(product_category)


@product_categories_router.post(
    "",
    response_model=OutputSingleProductCategoryModel,
    status_code=status.HTTP_201_CREATED,
    summary="Create product category"
)
def create_product_category(
    decoded_token: dict = Depends(verify_authorization_token),
    product_category_model: InputCreateProductCategoryModel = Body()
):
    product_category = ProductCategory(
        **product_category_model.dict(),
        created_by=decoded_token["id"]
    )

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
