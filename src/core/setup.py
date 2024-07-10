from fastapi import FastAPI
from fastapi.responses import ORJSONResponse
from fastapi.middleware.cors import CORSMiddleware

from core.config import settings
from core.lifespan import lifespan
from apps.user import user_router


def setup_app() -> FastAPI:
    """Set functionality for API"""

    app: FastAPI = FastAPI(
        default_response_class=ORJSONResponse,
        title=settings.run.app_title,
        lifespan=lifespan,
        settings=settings,
    )
    app.add_middleware(
        middleware_class=CORSMiddleware,
        allow_origins=settings.cors.origins,
        allow_credentials=True,
        allow_methods=settings.cors.methods,
        allow_headers=settings.cors.headers,
    )

    app.include_router(user_router)

    return app
