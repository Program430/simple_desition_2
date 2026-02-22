from contextlib import AbstractAsyncContextManager
from typing import Any, Callable, Type

from fastapi import FastAPI

from starlette.middleware.base import BaseHTTPMiddleware
from src.share.core.config import settings
from src.web.api.api_v1 import api_v1


Lifespan = Callable[[FastAPI], AbstractAsyncContextManager[Any]]


def get_app(
    lifespan: Lifespan | None = None,
    middlewares: list[Type[BaseHTTPMiddleware]] | None = None,
) -> FastAPI:
    app = FastAPI(
        title="Ticker price api",
        description="Ticker price api",
        version=settings.api_version,
        docs_url="/docs" if settings.debug else None,       
        redoc_url="/redoc" if settings.debug else None,     
        openapi_url="/openapi.json" if settings.debug else None,
        lifespan=lifespan 
    )
    
    if middlewares:
        for middleware in middlewares:
            app.add_middleware(middleware)
            
    app.include_router(api_v1)
            
    return app