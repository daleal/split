from pydantic import UUID4, StrictFloat

from split.shared.schemas import BaseSchema


class ConsumptionCreateOrUpdateSchema(BaseSchema):
    amount: StrictFloat
    participant_id: UUID4
    item_id: UUID4


class ConsumptionResponseSchema(BaseSchema):
    id: UUID4
    amount: StrictFloat
    participant_id: UUID4
    item_id: UUID4
