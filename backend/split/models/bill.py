import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel

if TYPE_CHECKING:
    from split.models import Item, Participant


class Bill(BaseModel):
    __tablename__ = "bills"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    images = Column(ARRAY(String), default=list)
    generating_items = Column(Boolean, default=False, nullable=False)
    generation_successful = Column(Boolean, default=False, nullable=True)

    items = relationship("Item", back_populates="bill", uselist=True)
    participants = relationship("Participant", back_populates="bill", uselist=True)

    @property
    def image(self) -> str | None:
        if not self.images:
            return None
        return self.images[-1]
