from fastapi import APIRouter, Depends
from pydantic import UUID4
from sqlalchemy.orm import Session

import split.crud.bills as bills_crud
from split import deps
from split.schemas.admin.bill import BillDetailResponseSchema, BillListResponseSchema

router = APIRouter()


@router.get("", response_model=list[BillListResponseSchema])
def get_all_bills(db: Session = Depends(deps.get_db)) -> list[BillListResponseSchema]:
    bills = bills_crud.get_all(db)
    return [BillListResponseSchema.from_orm(x) for x in bills]


@router.get("/{bill_id}", response_model=BillDetailResponseSchema)
def get_bill(
    bill_id: UUID4, db: Session = Depends(deps.get_db)
) -> BillDetailResponseSchema:
    return BillDetailResponseSchema.from_orm(bills_crud.get_by_id(db, bill_id))
