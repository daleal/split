from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from split.config import settings
from split.database import engine
from split.endpoints.bills import router as bills_router
from split.endpoints.shared import router as shared_router
from split.shared.models import BaseModel

BaseModel.metadata.create_all(bind=engine)

app = FastAPI()


app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


app.include_router(bills_router, prefix="/bills", tags=["Bills"])
app.include_router(shared_router, tags=["Shared"])
