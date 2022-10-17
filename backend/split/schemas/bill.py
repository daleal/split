from pydantic import UUID4, StrictBool, StrictStr

from split.shared.schemas import BaseSchema


class BillUpdateSchema(BaseSchema):
    image: StrictStr


class BillResponseSchema(BaseSchema):
    id: UUID4
    image: StrictStr | None
    generating_items: StrictBool
    generation_successful: StrictBool | None
