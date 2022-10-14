from pydantic import UUID4, StrictFloat, StrictInt

from split.shared.schemas import BaseSchema


class ConsumptionCreateOrUpdateSchema(BaseSchema):
    amount: StrictFloat | StrictInt


class ConsumptionResponseSchema(BaseSchema):
    id: UUID4
    amount: StrictFloat
    participant_id: UUID4
    item_id: UUID4
