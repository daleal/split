from __future__ import annotations

import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel

if TYPE_CHECKING:
    from split.models import Item, ItemGeneration, Participant


class Bill(BaseModel):
    __tablename__ = "bills"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    images = Column(ARRAY(String), default=list)

    items = relationship("Item", back_populates="bill", uselist=True)
    item_generations = relationship(
        "ItemGeneration",
        back_populates="bill",
        uselist=True,
    )
    participants = relationship("Participant", back_populates="bill", uselist=True)

    @property
    def image(self) -> str | None:
        if not self.images:
            return None
        return self.images[-1]

    @property
    def item_generation(self) -> ItemGeneration | None:
        if not self.item_generations:
            return None
        return self.item_generations[-1]

    @property
    def generating_items(self) -> bool:
        if self.item_generation is None:
            return False
        return self.item_generation.running

    @property
    def generation_successful(self) -> bool | None:
        if self.item_generation is None:
            return None
        return self.item_generation.generation_successful
