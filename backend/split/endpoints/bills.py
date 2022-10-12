from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
import split.crud.items as items_crud
from split import deps
from split.schemas.bill import BillResponseSchema, BillUpdateSchema
from split.schemas.item import ItemCreateSchema
from split.services.receipt_scanner import extract_relevant_information

router = APIRouter()


@router.get("", response_model=list[BillResponseSchema])
def get_all_bills(db: Session = Depends(deps.get_db)) -> list[BillResponseSchema]:
    bills = bills_crud.get_all(db)
    return list(bills)


@router.post("", response_model=BillResponseSchema)
def create_bill(db: Session = Depends(deps.get_db)) -> BillResponseSchema:
    return bills_crud.create(db)


@router.get("/{bill_id}", response_model=BillResponseSchema)
def get_bill(bill_id: UUID4, db: Session = Depends(deps.get_db)) -> BillResponseSchema:
    return bills_crud.get_by_id(db, bill_id)


@router.post("/{bill_id}/image", response_model=BillResponseSchema)
def attach_image_to_bill(
    bill_id: UUID4, bill_schema: BillUpdateSchema, db: Session = Depends(deps.get_db)
) -> BillResponseSchema:
    bill = bills_crud.get_by_id(db, bill_id)
    return bills_crud.attach_image(db, bill, bill_schema.image)


@router.post("/{bill_id}/items", response_model=BillResponseSchema)
def generate_items_for_bill(
    bill_id: UUID4, db: Session = Depends(deps.get_db)
) -> BillResponseSchema:
    bill = bills_crud.get_by_id(db, bill_id)
    if bill.image is None:
        return bill
    bill.items = []
    extracted = extract_relevant_information(bill.image)
    for raw_item in extracted:
        item = items_crud.create(db, ItemCreateSchema(**raw_item))
        bill.items.append(item)
        db.commit()
    db.refresh(bill)
    return bill
