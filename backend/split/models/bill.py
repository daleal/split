import uuid

from sqlalchemy import Column, String
from sqlalchemy.dialects.postgresql import ARRAY, UUID

from split.shared.models import BaseModel


class Bill(BaseModel):
    __tablename__ = "bills"

    id = Column(UUID(as_uuid=True), primary_key=True, index=True, default=uuid.uuid4)
    images = Column(ARRAY(String), default=list)

    @property
    def image(self) -> str | None:
        if not self.images:
            return None
        return self.images[-1]
