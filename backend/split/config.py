import os
from typing import List


class Settings:
    database_url: str = os.environ["DATABASE_URL"].replace(
        "postgres://", "postgresql://"
    )
    allowed_origins: List[str] = list(
        filter(lambda x: x, os.environ.get("ALLOWED_ORIGINS", "").split(" "))
    )


settings = Settings()
