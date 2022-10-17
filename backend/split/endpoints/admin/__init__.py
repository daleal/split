from fastapi import APIRouter

from split.endpoints.admin.bills import router as bills_router

router = APIRouter(tags=["Admin"])


router.include_router(bills_router, prefix="/bills")
