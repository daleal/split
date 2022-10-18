from pydantic import UUID4, StrictBool, StrictStr

from split.shared.schemas import BaseSchema


class BillUpdateSchema(BaseSchema):
    image: StrictStr


class BillResponseSchema(BaseSchema):
    id: UUID4
    image: StrictStr | None
    running_item_generation: StrictBool
    image_found: StrictBool | None
    borders_detected: StrictBool | None
    generation_successful: StrictBool | None
