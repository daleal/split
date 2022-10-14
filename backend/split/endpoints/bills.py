from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
from split import deps
from split.schemas.bill import BillResponseSchema, BillUpdateSchema

router = APIRouter()


@router.get("", response_model=list[BillResponseSchema])
def get_all_bills(db: Session = Depends(deps.get_db)) -> list[BillResponseSchema]:
    bills = bills_crud.get_all(db)
    return [BillResponseSchema.from_orm(x) for x in bills]


@router.post("", response_model=BillResponseSchema)
def create_bill(db: Session = Depends(deps.get_db)) -> BillResponseSchema:
    return BillResponseSchema.from_orm(bills_crud.create(db))


@router.get("/{bill_id}", response_model=BillResponseSchema)
def get_bill(bill_id: UUID4, db: Session = Depends(deps.get_db)) -> BillResponseSchema:
    return BillResponseSchema.from_orm(bills_crud.get_by_id(db, bill_id))


@router.post("/{bill_id}/image", response_model=BillResponseSchema)
def attach_image_to_bill(
    bill_id: UUID4, bill_schema: BillUpdateSchema, db: Session = Depends(deps.get_db)
) -> BillResponseSchema:
    bill = bills_crud.get_by_id(db, bill_id)
    return BillResponseSchema.from_orm(
        bills_crud.attach_image(db, bill, bill_schema.image)
    )
