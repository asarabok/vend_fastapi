from authentication import JwtAuthentication
from db_models import Machine, User
from dependencies import get_db, verify_authorization_token
from dto_models import (
    AuthenticatedUserResponseModel,
    BaseUserModel,
    LoginUserModel,
    UserInfoModel
)
from fastapi import APIRouter, Body, Depends, HTTPException, status
from sqlalchemy.orm import Session
from utils import hash_password

from endpoints.v1.users.mappers import map_to_output_machine_model

user_routers = APIRouter(prefix="/users", tags=["User"])


@user_routers.post(
    "/login",
    response_model=AuthenticatedUserResponseModel,
    summary="User login which generates JWT token"
)
def user_login(
    session: Session = Depends(get_db),
    user: LoginUserModel = Body()
):
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


@user_routers.get(
    "/me",
    response_model=UserInfoModel,
    summary="Get logged user info and assigned machines"
)
def get_user_data(
    session: Session = Depends(get_db),
    decoded_token: dict = Depends(verify_authorization_token)
):
    user_assigned_machines = session.query(
        Machine
    ).filter(
        Machine.owner_id == decoded_token["id"]
    ).all()

    output_user_machines = [
        map_to_output_machine_model(m)
        for m in user_assigned_machines
    ]

    return UserInfoModel(
        user=BaseUserModel(**decoded_token),
        assigned_machines=output_user_machines
    )
