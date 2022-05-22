from dto_models import (
    BaseUserModel
)


def map_to_base_user_model(user):
    return BaseUserModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )
