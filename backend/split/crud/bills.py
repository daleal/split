from typing import Literal, overload

from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from split.models import Bill


def get_all(db: Session) -> list[Bill]:
    return list(db.query(Bill).all())


@overload
def get_by_id(db: Session, bill_id: UUID4, silent: Literal[False]) -> Bill:
    ...


@overload
def get_by_id(db: Session, bill_id: UUID4) -> Bill:
    ...


@overload
def get_by_id(db: Session, bill_id: UUID4, silent: Literal[True]) -> Bill | None:
    ...


@overload
def get_by_id(db: Session, bill_id: UUID4, silent: bool) -> Bill | None:
    ...


def get_by_id(db: Session, bill_id: UUID4, silent: bool = False) -> Bill | None:
    bill = db.query(Bill).filter(Bill.id == bill_id).first()
    if not silent and bill is None:
        raise HTTPException(
            status_code=404,
            detail=f"No bill found with id {bill_id}",
        )
    return bill


def create(db: Session) -> Bill:
    bill = Bill()
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def attach_image(db: Session, bill: Bill, image: str) -> Bill:
    bill.images = [*bill.images, image]
    db.commit()
    db.refresh(bill)
    return bill
