import hashlib

from database import session
from db_models import ProductCategory, User


def hash_password(password):
    d = hashlib.sha3_256(password.encode())
    return d.hexdigest()


def get_product_categories_query():
    return session.query(
        ProductCategory
    ).order_by(ProductCategory.title.asc())


def get_login_user(user):
    return session.query(
        User
    ).filter(
        User.email == user.email, User.password == hash_password(user.password)
    ).one_or_none()
