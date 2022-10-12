import uuid

from sqlalchemy import Column, ForeignKey, String
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import relationship

from split.shared.models import BaseModel


class Participant(BaseModel):
    __tablename__ = "participants"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    name = Column(String, nullable=False)

    bill_id = Column(UUID(as_uuid=True), ForeignKey("bills.id"))
    bill = relationship("Bill", back_populates="participants")
