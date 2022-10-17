from pydantic import UUID4, StrictInt, StrictStr

from split.schemas.consumption import ConsumptionResponseSchema
from split.shared.schemas import BaseSchema


class ItemCreateSchema(BaseSchema):
    description: StrictStr
    full_price: StrictInt
    amount: StrictInt | None
    position: StrictInt


class ItemResponseSchema(BaseSchema):
    id: UUID4
    description: StrictStr
    amount: StrictInt
    full_price: StrictInt
    individual_price: StrictInt
    position: StrictInt
    consumption: list[ConsumptionResponseSchema]
