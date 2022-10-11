from fastapi import APIRouter, Response

router = APIRouter()


@router.get("/health-check")
def health_check() -> Response:
    return Response(status_code=200)
