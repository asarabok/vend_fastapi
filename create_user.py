def create_user(first_name, last_name, email, password):
    try:
        create_user_model = CreateUserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hash_password(password)
        )
    except ValidationError as e:
        typer.echo(f"Create user error. Details: {e.json()}")
        return

    user = User(**create_user_model.dict())
    session.add(user)
    try:
        session.commit()
    except IntegrityError:
        typer.echo(f"Integrity error! User with email {email} already exists")
        return

    typer.echo(f"User {first_name} {last_name} successfully created!")


if __name__ == "__main__":
    import os
    import sys

    import typer
    from dotenv import load_dotenv

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    sys.path.append(BASE_DIR)

    from pydantic import ValidationError

    from database import session
    from db_models import User
    from dto_models import CreateUserModel
    from utils import hash_password
    from sqlalchemy.exc import IntegrityError

    typer.run(create_user)
