from pydantic import UUID4, StrictStr

from split.schemas.item import ItemResponseSchema
from split.shared.schemas import BaseSchema


class BillUpdateSchema(BaseSchema):
    image: StrictStr


class BillResponseSchema(BaseSchema):
    id: UUID4
    image: StrictStr | None
    items: list[ItemResponseSchema]
