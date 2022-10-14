from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.consumption as consumption_crud
from split import deps
from split.schemas.consumption import (
    ConsumptionCreateOrUpdateSchema,
    ConsumptionResponseSchema,
)
from split.services.receipt_scanner import extract_relevant_information

router = APIRouter()


@router.get("", response_model=list[ConsumptionResponseSchema])
def get_consumption(
    participant_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> list[ConsumptionResponseSchema]:
    consumption = consumption_crud.get_all(db, participant_id)
    return [ConsumptionResponseSchema.from_orm(x) for x in consumption]


@router.put("/{item_id}", response_model=ConsumptionResponseSchema)
def create_or_update_consumption(
    participant_id: UUID4,
    item_id: UUID4,
    consumption_schema: ConsumptionCreateOrUpdateSchema,
    db: Session = Depends(deps.get_db),
) -> ConsumptionResponseSchema:
    consumption = consumption_crud.get(db, participant_id, item_id, silent=True)
    if consumption is None:
        consumption = consumption_crud.create(
            db, participant_id, item_id, consumption_schema
        )
    else:
        consumption = consumption_crud.update(db, consumption, consumption_schema)
    return ConsumptionResponseSchema.from_orm(consumption)


@router.delete("/{item_id}")
def delete_consumption(
    participant_id: UUID4,
    item_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> None:
    consumption = consumption_crud.get(db, participant_id, item_id)
    consumption_crud.delete(db, consumption)
