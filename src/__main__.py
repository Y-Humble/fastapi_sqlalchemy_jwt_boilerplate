import uvicorn
from fastapi import FastAPI

from core.config import settings
from core.setup import setup_app

app: FastAPI = setup_app()


if __name__ == "__main__":
    uvicorn.run(
        app="main:app",
        host=settings.run.host,
        port=settings.run.port,
        reload=True,
        log_level=settings.run.log_level,
    )
