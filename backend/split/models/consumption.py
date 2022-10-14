import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Float, UniqueConstraint
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel

if TYPE_CHECKING:
    from split.models import Item, Participant


class Consumption(BaseModel):
    __tablename__ = "consumption"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    amount = Column(Float, nullable=False)

    participant_id = Column(UUID(as_uuid=True), ForeignKey("participants.id"))
    participant = relationship("Participant", back_populates="consumption")

    item_id = Column(UUID(as_uuid=True), ForeignKey("items.id"))
    item = relationship("Item", back_populates="consumption")
