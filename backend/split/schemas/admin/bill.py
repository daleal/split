from datetime import datetime

from pydantic import UUID4, StrictStr

from split.schemas.admin.item_generation import (
    ItemGenerationDetailResponseSchema,
    ItemGenerationListResponseSchema,
)
from split.shared.schemas import BaseSchema


class BillListResponseSchema(BaseSchema):
    id: UUID4
    updated_at: datetime
    image: StrictStr | None
    item_generation: ItemGenerationListResponseSchema | None


class BillDetailResponseSchema(BaseSchema):
    id: UUID4
    updated_at: datetime
    image: StrictStr | None
    item_generation: ItemGenerationDetailResponseSchema | None
