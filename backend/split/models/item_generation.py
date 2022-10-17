import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Boolean, Column, ForeignKey, Text
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from split.errors import NoRelevantItemsFoundError
from split.services.receipt_parser.core import (
    clean_string,
    extract_relevant_information,
)
from split.shared.models import BaseModel

if TYPE_CHECKING:
    from split.models import Bill


class ItemGeneration(BaseModel):
    __tablename__ = "item_generations"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    running = Column(Boolean, default=True, nullable=False)
    image_found = Column(Boolean, default=None, nullable=True)
    borders_detected = Column(Boolean, default=None, nullable=True)
    generation_successful = Column(Boolean, default=None, nullable=True)
    generated_text_lines_raw = Column(ARRAY(Text), default=None, nullable=True)

    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="item_generations")

    @property
    def generated_text_lines_clean(self) -> list[str]:
        if not self.generated_text_lines_raw:
            return []
        return list(
            filter(
                lambda clean_text: clean_text != "",
                map(clean_string, self.generated_text_lines_raw),
            )
        )

    @property
    def parsed_item_primitives(self) -> list[dict[str, str | int]]:
        if not self.generated_text_lines_raw:
            return []
        try:
            return extract_relevant_information(self.generated_text_lines_raw)
        except NoRelevantItemsFoundError:
            return []
