from pydantic import UUID4, StrictInt, StrictStr

from split.shared.schemas import BaseSchema


class ItemCreateSchema(BaseSchema):
    description: StrictStr
    full_price: StrictInt
    amount: StrictInt | None


class ItemResponseSchema(BaseSchema):
    id: UUID4
    description: StrictStr
    amount: StrictInt
    full_price: StrictInt
    individual_price: StrictInt
