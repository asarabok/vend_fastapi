from dto_models import BaseUserModel, OutputMachineModel


def map_to_base_user_model(user):
    return BaseUserModel(
        id=user.id,
        first_name=user.first_name,
        last_name=user.last_name,
        email=user.email
    )


def map_to_output_machine_model(machine):
    return OutputMachineModel(
        id=machine.id,
        manufacturer=machine.manufacturer,
        name=machine.name,
        model=machine.model
    )
