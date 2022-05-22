from dto_models import BaseUserModel, OutputProductCategoryModel


def map_to_base_user_model(user):
    return BaseUserModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )


def map_to_output_product_category_model(product_category):
    return OutputProductCategoryModel(
        id=product_category.id,
        title=product_category.title
    )
