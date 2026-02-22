from src.web.lifespan import lifespan
from src.web.middleware import LoggingMiddleware
from src.web.setup import get_app


app = get_app(
    lifespan=lifespan,
    middlewares=[
        LoggingMiddleware
    ]
)
