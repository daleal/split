from sqlalchemy.orm import Session

from split.models import ItemGeneration


def create(db: Session) -> ItemGeneration:
    item_generation = ItemGeneration()
    db.add(item_generation)
    db.commit()
    db.refresh(item_generation)
    return item_generation
