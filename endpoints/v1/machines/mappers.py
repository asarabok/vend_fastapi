from dto_models import OutputMachineColumnModel, OutputMachineListModel
from endpoints.v1.products.mappers import map_to_output_single_product_model
from endpoints.v1.users.mappers import map_to_base_user_model


def map_to_output_machine_column(machine_column):
    return OutputMachineColumnModel(
        index=machine_column.index,
        current_quantity=machine_column.current_quantity,
        spiral_quantity=machine_column.spiral_quantity,
        price=machine_column.price,
        product=map_to_output_single_product_model(machine_column.product)
    )


def map_to_output_single_machine_model(machine):
    return OutputMachineListModel(
        id=machine.id,
        manufacturer=machine.manufacturer,
        name=machine.name,
        model=machine.model,
        owner=map_to_base_user_model(machine.owner),
        columns=[
            map_to_output_machine_column(mc)
            for mc in machine.columns
        ] if machine.columns else []
    )
