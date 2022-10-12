from pydantic import UUID4, StrictStr

from split.shared.schemas import BaseSchema


class ParticipantCreateSchema(BaseSchema):
    name: StrictStr


class ParticipantResponseSchema(BaseSchema):
    id: UUID4
    name: StrictStr
