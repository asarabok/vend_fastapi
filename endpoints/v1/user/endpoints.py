from authentication import JwtAuthentication
from db_models import User
from dependencies import verify_authorization_token
from dto_models import (
    AuthenticatedUserResponseModel,
    BaseUserModel,
    LoginUserModel
)
from fastapi import APIRouter, Depends, HTTPException, status
from utils import hash_password
from database import session

user_router = APIRouter(prefix="/user", tags=["User"])


@user_router.post(
    "/login",
    response_model=AuthenticatedUserResponseModel,
    summary="User login which generates JWT token"
)
def user_login(user: LoginUserModel):
    login_user = session.query(
        User
    ).filter(
        User.email == user.email, User.password == hash_password(user.password)
    ).one_or_none()

    if not login_user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong user data!"
        )

    token = JwtAuthentication.generate_jwt_token(login_user)
    return AuthenticatedUserResponseModel(token=token)


@user_router.get(
    "/me",
    response_model=BaseUserModel,
    summary="Get logged user data"
)
def get_user_data(
    decoded_token: dict = Depends(verify_authorization_token)
):
    return BaseUserModel(**decoded_token)
