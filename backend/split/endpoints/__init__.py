from fastapi import APIRouter

from split.endpoints.bills import router as bills_router
from split.endpoints.consumption import router as consumption_router
from split.endpoints.items import router as items_router
from split.endpoints.participants import router as participants_router
from split.endpoints.shared import router as shared_router

router = APIRouter()


router.include_router(bills_router, prefix="/bills", tags=["Bills"])
router.include_router(
    participants_router,
    prefix="/bills/{bill_id}/participants",
    tags=["Participants"],
)
router.include_router(
    items_router,
    prefix="/bills/{bill_id}/items",
    tags=["Items"],
)
router.include_router(
    consumption_router,
    prefix="/participants/{participant_id}/consumption",
    tags=["Consumption"],
)
router.include_router(shared_router, tags=["Shared"])
