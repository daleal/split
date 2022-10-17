import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel

if TYPE_CHECKING:
    from split.models import Bill, Consumption


class Item(BaseModel):
    __tablename__ = "items"

    DEFAULT_AMOUNT = 1

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    description = Column(String, nullable=False)
    amount = Column(Integer, nullable=False)
    full_price = Column(Integer, nullable=False)
    position = Column(Integer, default=0, nullable=False)

    consumption = relationship("Consumption", back_populates="item", uselist=True)

    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="items")

    def __init__(
        self,
        description: str,
        full_price: int,
        position: int = 0,
        amount: int | None = None,
    ) -> None:
        self.description = description
        self.full_price = full_price
        self.amount = amount or self.DEFAULT_AMOUNT
        self.position = position

    @property
    def individual_price(self) -> int:
        return int(self.full_price / self.amount)
