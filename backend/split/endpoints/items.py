from fastapi import APIRouter, BackgroundTasks, Depends, HTTPException
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
import split.crud.items as items_crud
from split import deps
from split.schemas.bill import BillResponseSchema
from split.schemas.item import ItemResponseSchema
from split.tasks.bills import generate_items_task

router = APIRouter()


@router.get("", response_model=list[ItemResponseSchema])
def get_all_items_from_bill(
    bill_id: UUID4,
    db: Session = Depends(deps.get_db),
) -> list[ItemResponseSchema]:
    items = items_crud.get_all_by_bill_id(db, bill_id)
    return [
        ItemResponseSchema.from_orm(x) for x in sorted(items, key=lambda x: x.position)
    ]


@router.post("/generate", response_model=BillResponseSchema)
async def generate_items(
    bill_id: UUID4,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db),
) -> BillResponseSchema:
    bill = bills_crud.get_by_id(db, bill_id)
    if bill.image is None:
        raise HTTPException(
            status_code=409,
            detail=f"No image has been uploaded for bill with id {bill_id}",
        )
    if bill.generating_items:
        raise HTTPException(
            status_code=409,
            detail=f"The bill with id {bill_id} is currently being processed",
        )
    bill.generating_items = True
    bill.generation_successful = None
    db.commit()
    background_tasks.add_task(generate_items_task, db, bill)
    return BillResponseSchema.from_orm(bill)
