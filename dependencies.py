from typing import Generator

from fastapi import Header, HTTPException, status
from jwt.exceptions import DecodeError, ExpiredSignatureError

from authentication import JwtAuthentication
from database import session


def verify_authorization_token(authorization: str = Header(default=None)) -> dict:
    if not authorization:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Please provide authorization token in header!"
        )
    token = JwtAuthentication.get_token_from_header(authorization)

    try:
        decoded = JwtAuthentication.read_jwt_token(token)

    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired!"
        )

    except DecodeError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Wrong token!"
        )

    return decoded


def get_db() -> Generator:
    try:
        db = session()
        yield db
    finally:
        db.close()
