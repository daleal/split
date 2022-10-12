import uuid

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel


class Item(BaseModel):
    __tablename__ = "items"

    DEFAULT_DESCRIPTION = "Unknown Item"
    DEFAULT_AMOUNT = 1
    DEFAULT_FULL_PRICE = 6666

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    full_price = Column(Integer, nullable=False)

    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="items")

    def __init__(
        self,
        description: str | None = None,
        amount: int | None = None,
        full_price: int | None = None,
    ) -> None:
        self.description = description or self.DEFAULT_DESCRIPTION
        self.amount = amount or self.DEFAULT_AMOUNT
        self.full_price = full_price or self.DEFAULT_FULL_PRICE

    @property
    def individual_price(self) -> int:
        return int(self.full_price / self.amount)
