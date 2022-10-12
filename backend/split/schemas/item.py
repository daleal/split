from pydantic import UUID4, StrictInt, StrictStr

from split.shared.schemas import BaseSchema


class ItemCreateSchema(BaseSchema):
    description: StrictStr | None
    amount: StrictInt | None
    full_price: StrictInt | None


class ItemResponseSchema(BaseSchema):
    id: UUID4
    description: StrictStr
    amount: StrictInt
    full_price: StrictInt
    individual_price: StrictInt
