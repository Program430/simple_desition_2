from fastapi import APIRouter

from .routers import ticker_price_router

api_v1 = APIRouter()

api_v1.include_router(ticker_price_router)
