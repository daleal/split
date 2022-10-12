import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    full_price = Column(Integer, nullable=False)

    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="items")

    @property
    def individual_price(self) -> int:
        return int(self.full_price / self.amount)
