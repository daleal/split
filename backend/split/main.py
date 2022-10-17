from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from split.config import settings
from split.database import engine
from split.endpoints import router as main_router
from split.endpoints.admin import router as admin_router
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


app.include_router(admin_router, prefix="/admin")
app.include_router(main_router)
