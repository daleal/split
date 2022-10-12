from pydantic import UUID4
from sqlalchemy.orm import Session

from split.models import Item
from split.schemas.item import ItemCreateSchema


def get_all_by_bill_id(db: Session, bill_id: UUID4) -> list[Item]:
    return list(db.query(Item).filter(Item.bill_id == bill_id))


def create(db: Session, item_schema: ItemCreateSchema) -> Item:
    item = Item(**item_schema.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
