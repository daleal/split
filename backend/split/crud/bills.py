from fastapi import HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

from split.models.bill import Bill as BillModel


def get_by_id(db: Session, bill_id: UUID4, silent: bool = False) -> BillModel:
    bill = db.query(BillModel).filter(BillModel.id == bill_id).first()
    if not silent and not bill:
        raise HTTPException(
            status_code=404,
            detail=f"No bill found with id {bill_id}",
        )
    return bill


def create(db: Session) -> BillModel:
    bill = BillModel()
    db.add(bill)
    db.commit()
    db.refresh(bill)
    return bill


def attach_image(db: Session, bill: BillModel, image: str) -> BillModel:
    bill.images = [*bill.images, image]
    db.commit()
    db.refresh(bill)
    return bill
