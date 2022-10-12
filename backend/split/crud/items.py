from sqlalchemy.orm import Session

from split.models import Item
from split.schemas.item import ItemCreateSchema


def create(db: Session, item_schema: ItemCreateSchema) -> Item:
    item = Item(**item_schema.dict())
    db.add(item)
    db.commit()
    db.refresh(item)
    return item
