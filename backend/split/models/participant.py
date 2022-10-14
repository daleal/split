import uuid
from typing import TYPE_CHECKING

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel

if TYPE_CHECKING:
    from split.models import Bill, Consumption


class Participant(BaseModel):
    __tablename__ = "participants"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    consumption = relationship(
        "Consumption", back_populates="participant", uselist=True
    )

    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="participants")
