from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.share.database.setup import auto_commit_session_gen
from src.share.repository.ticker_price_repository import TickerPriceRepository
from src.web.domain.ticker_price_service import TickerPriceService


def ticker_price_repository_depend(session: AsyncSession = Depends(auto_commit_session_gen)) -> TickerPriceRepository:
    return TickerPriceRepository(session)


def ticker_price_service_depend(ticker_price_repository: TickerPriceRepository = Depends(ticker_price_repository_depend)) -> TickerPriceService:
    return TickerPriceService(ticker_price_repository)
