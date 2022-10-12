from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
import split.crud.items as items_crud
from split import deps
from split.schemas.item import ItemCreateSchema, ItemResponseSchema
from split.services.receipt_scanner import extract_relevant_information

router = APIRouter()


@router.get("", response_model=list[ItemResponseSchema])
def get_all_items_from_bill(
    bill_id: UUID4, db: Session = Depends(deps.get_db),
) -> list[ItemResponseSchema]:
    items = items_crud.get_all_by_bill_id(db, bill_id)
    return list(items)


@router.post("/generate", response_model=list[ItemResponseSchema])
def generate_items(
    bill_id: UUID4, db: Session = Depends(deps.get_db)
) -> list[ItemResponseSchema]:
    bill = bills_crud.get_by_id(db, bill_id)
    if bill.image is None:
        return []
    extracted = extract_relevant_information(bill.image)
    items = [items_crud.create(db, ItemCreateSchema(**x)) for x in extracted]
    bill.items = items
    db.commit()
    return list(items)
