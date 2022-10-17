from pydantic import UUID4, StrictBool, StrictInt, StrictStr

from split.shared.schemas import BaseSchema


class ItemGenerationListResponseSchema(BaseSchema):
    id: UUID4
    running: StrictBool
    image_found: StrictBool | None
    borders_detected: StrictBool | None
    generation_successful: StrictBool | None


class ItemGenerationDetailResponseSchema(ItemGenerationListResponseSchema):
    generated_text_lines_raw: list[StrictStr]
    generated_text_lines_clean: list[StrictStr]
    parsed_item_primitives: list[dict[StrictStr, StrictStr | StrictInt]]
