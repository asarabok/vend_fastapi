from db_models import Machine, MachineColumn, Product
from dependencies import get_db, verify_authorization_token
from dto_models import (
    InputMachinePlanogramChangeModel
)
from fastapi import APIRouter, Body, Depends, HTTPException, Path, status
from pagination import (
    PaginatedMetaModel,
    PaginatedResponseModel,
    Pagination,
    PaginationInputModel
)
from sqlalchemy.orm import Session, joinedload

from endpoints.v1.machines.mappers import (
    map_to_output_single_machine_model
)

machines_router = APIRouter(
    prefix="/machines", tags=["Machine"])


@machines_router.get(
    "",
    response_model=PaginatedResponseModel,
    summary="Get paginated machines"
)
def get_machines(
    session: Session = Depends(get_db),
    pagination: PaginationInputModel = Depends(),
    decoded_token: dict = Depends(verify_authorization_token)
):
    machines_query = session.query(
        Machine
    ).options(
        joinedload(Machine.owner)
    ).options(
        joinedload(
            Machine.columns
            ).joinedload(
                MachineColumn.product
                ).joinedload(
                    Product.product_category
                )
    ).order_by(
        Machine.id.desc()
    )

    machines = Pagination.paginate_query(
        machines_query, pagination.page, pagination.page_size)
    total_items, num_pages = Pagination.get_total_items_and_pages(
        machines_query, pagination.page_size)

    output_machines = [
        map_to_output_single_machine_model(m)
        for m in machines
    ]

    output_meta = PaginatedMetaModel(
        page=pagination.page,
        page_size=pagination.page_size,
        num_pages=num_pages,
        total_items=total_items
    )
    return PaginatedResponseModel(
        meta=output_meta, content=output_machines)


@machines_router.post(
    "/{item_id}/push-planogram",
    summary="Push machine planogram. Only owner of machine can make this change"
)
def push_planogram_to_machine(
    session: Session = Depends(get_db),
    decoded_token: dict = Depends(verify_authorization_token),
    item_id: int = Path(title="Machine ID"),
    planogram_model: InputMachinePlanogramChangeModel = Body()
):
    machine_owner_id = session.query(
        Machine.owner_id).filter(Machine.id == item_id).limit(1).scalar()

    if not machine_owner_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Machine with ID {item_id} does not exists!")

    if not machine_owner_id == decoded_token["id"]:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Only machine owner can push planogram!"
        )

    machine_columns = session.query(
        MachineColumn
    ).filter(
        MachineColumn.machine_id == item_id
    ).all()

    for mc in planogram_model.columns:
        product = session.query(
            Product
        ).filter(
            Product.id == mc.product_id
        ).first()

        if not product:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Product with ID {mc.product_id} doesn't exists!"
            )

    for mc in machine_columns:
        session.delete(mc)

    session.commit()

    i = 0
    for mc in planogram_model.columns:
        machine_column = MachineColumn(
            index=i,
            current_quantity=20,
            spiral_quantity=20,
            price=mc.price,
            product_id=mc.product_id,
            machine_id=item_id
        )
        i += 1
        session.add(machine_column)

    session.commit()

    return {
        "message": "Planogram successfully updated!"
    }
