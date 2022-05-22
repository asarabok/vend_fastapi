from dto_models import (
    OutputListProductCategoryModel,
    OutputSingleProductCategoryModel
)


def map_to_output_product_category_list_model(product_category):
    return OutputListProductCategoryModel(
        id=product_category.id,
        title=product_category.title,
        created_at=product_category.created_at
    )


def map_to_output_single_product_category_model(product_category):
    return OutputSingleProductCategoryModel(
        id=product_category.id,
        title=product_category.title,
        created_by=product_category.created_by,
        updated_by=product_category.updated_by,
        created_at=product_category.created_at,
        updated_at=product_category.updated_at
    )
