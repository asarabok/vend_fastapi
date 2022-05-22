import os
from datetime import datetime, timedelta, timezone

import jwt
from fastapi import HTTPException, status

from endpoints.v1.users.mappers import map_to_base_user_model


class JwtAuthentication:
    @classmethod
    def generate_jwt_token(cls, user):
        mapped_user = map_to_base_user_model(user)
        exp_token = datetime.now(
            timezone.utc) + timedelta(
                days=int(os.environ['JWT_EXPIRE_DAYS']))

        return jwt.encode(
            {**mapped_user.dict(), "exp": exp_token},
            os.environ['SECRET'],
            algorithm=os.environ['JWT_ALGORITHM']
        )

    @classmethod
    def get_token_from_header(cls, authorization_header):
        token_parts = authorization_header.split()

        if token_parts[0].lower() != "bearer":
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header must start with Bearer")

        elif len(token_parts) == 1:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid authorization token ")

        elif len(token_parts) > 2:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Authorization header must be Bearer token")

        return token_parts[1]

    @classmethod
    def read_jwt_token(cls, token):
        return jwt.decode(
            token, os.environ['SECRET'],
            algorithms=os.environ['JWT_ALGORITHM']
        )
