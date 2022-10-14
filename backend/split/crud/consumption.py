from typing import Literal, overload

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from split.models import Consumption
from split.schemas.consumption import ConsumptionCreateOrUpdateSchema


def get_all(db: Session, participant_id: UUID4) -> list[Consumption]:
    return list(
        db.query(Consumption).filter(Consumption.participant_id == participant_id)
    )


@overload
def get(
    db: Session,
    participant_id: UUID4,
    item_id: UUID4,
    silent: Literal[False],
) -> Consumption:
    ...


@overload
def get(db: Session, participant_id: UUID4, item_id: UUID4) -> Consumption:
    ...


@overload
def get(
    db: Session,
    participant_id: UUID4,
    item_id: UUID4,
    silent: Literal[True],
) -> Consumption | None:
    ...


@overload
def get(
    db: Session,
    participant_id: UUID4,
    item_id: UUID4,
    silent: bool,
) -> Consumption | None:
    ...


def get(
    db: Session,
    participant_id: UUID4,
    item_id: UUID4,
    silent: bool = False,
) -> Consumption | None:
    consumption = (
        db.query(Consumption)
        .filter(
            Consumption.participant_id == participant_id
            and Consumption.item_id == item_id
        )
        .first()
    )
    if not silent and consumption is None:
        raise HTTPException(
            status_code=404,
            detail=(
                f"No consumption found with participant id {participant_id} "
                f"and item id {item_id}"
            ),
        )
    return consumption


def create(
    db: Session,
    participant_id: UUID4,
    item_id: UUID4,
    consumption_schema: ConsumptionCreateOrUpdateSchema,
) -> Consumption:
    consumption = Consumption(
        participant_id=str(participant_id),
        item_id=str(item_id),
        **consumption_schema.dict(),
    )
    db.add(consumption)
    db.commit()
    db.refresh(consumption)
    return consumption


def update(
    db: Session,
    consumption: Consumption,
    consumption_schema: ConsumptionCreateOrUpdateSchema,
) -> Consumption:
    for key, value in consumption_schema.dict(exclude_unset=True).items():
        setattr(consumption, key, value)
    db.commit()
    db.refresh(consumption)
    return consumption


def delete(db: Session, consumption: Consumption) -> None:
    db.delete(consumption)
    db.commit()
