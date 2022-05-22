from db_models import Machine
from dto_models import InputMachineModel


def create_user(first_name, last_name, email, password):
    try:
        create_user_model = CreateUserModel(
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password
        )
    except ValidationError as e:
        typer.echo(f"Create user error. Details: {e.json()}")
        return

    create_user_model.password = hash_password(create_user_model.password)
    user = User(**create_user_model.dict())
    session.add(user)

    try:
        session.commit()
    except IntegrityError:
        typer.echo(f"Integrity error! User with email {email} already exists")
        return

    user_id = user.id
    typer.echo(f"User {first_name} {last_name} successfully created!")
    session.flush()

    try:
        create_machine_model = InputMachineModel(
            manufacturer=f"{create_user_model.first_name} Systems",
            name=f"{create_user_model.first_name}'s Machine",
            model="Ultra",
            owner_id=user_id
        )
    except ValidationError as e:
        typer.echo(f"Create machine error. Details: {e.json()}")
        return

    machine = Machine(**create_machine_model.dict())
    session.add(machine)
    session.commit()

    typer.echo(f"Machine {machine.name} successfully created!")


if __name__ == "__main__":
    import os
    import sys

    import typer
    from dotenv import load_dotenv

    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    load_dotenv(os.path.join(BASE_DIR, '.env'))
    sys.path.append(BASE_DIR)

    from pydantic import ValidationError
    from sqlalchemy.exc import IntegrityError

    from database import session
    from db_models import User
    from dto_models import CreateUserModel
    from utils import hash_password

    typer.run(create_user)
