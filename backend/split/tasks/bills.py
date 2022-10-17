from fastapi import Depends
from receipt_scanner.image.errors import NoContourFoundError
from sqlalchemy.orm import Session

import split.crud.items as items_crud
from split import deps
from split.models import Bill
from split.schemas.item import ItemCreateSchema
from split.services.receipt_scanner import extract_relevant_information


def generate_items_task(db: Session, bill: Bill) -> None:
    bill.generating_items = False
    bill.generation_successful = True
    if bill.image is None:
        bill.generation_successful = False
    else:
        try:
            extracted = extract_relevant_information(bill.image)
            items = [items_crud.create(db, ItemCreateSchema(**x)) for x in extracted]
            bill.items = items
            if not extracted:
                bill.generation_successful = False
        except NoContourFoundError:
            bill.generation_successful = False
    db.commit()
