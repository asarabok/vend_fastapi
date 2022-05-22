from dto_models import OutputProductListModel, OutputSingleProductModel

from endpoints.v1.product_categories.mappers import (
    map_to_output_single_product_category_model
)


def map_to_output_single_product_model(product):
    return OutputSingleProductModel(
        id=product.id,
        title=product.title,
        created_at=product.created_at,
        product_category=map_to_output_single_product_category_model(
            product.product_category
        )
    )


def map_to_output_product_list_model(product):
    return OutputProductListModel(
        id=product.id,
        title=product.title,
        created_at=product.created_at,
        product_category=map_to_output_single_product_category_model(
            product.product_category
        )
    )
