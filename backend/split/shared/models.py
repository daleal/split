from sqlalchemy import TIMESTAMP, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql import func


class Base:
    updated_at = Column(
        TIMESTAMP,
        server_default=func.now(),
        onupdate=func.current_timestamp(),
    )


BaseModel = declarative_base(cls=Base)
