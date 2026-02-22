from datetime import datetime
from src.share.repository.ticker_price_repository import TickerPriceRepository
from src.share.domain.ticker_price_entity import TickerPrice
from src.share.domain.ticker_value_object import Ticker


class TickerPriceService:
    def __init__(
        self,
        ticker_price_repository: TickerPriceRepository
    ):
        self.ticker_price_repository = ticker_price_repository

    async def get_ticker_price_chunk(
        self,
        ticker: Ticker,
        start_date: datetime,
        limit: int
    ) -> list[TickerPrice]:
        return await self.ticker_price_repository.get_chunk(ticker, start_date, limit)

    async def get_last_ticker_price(self, ticker: Ticker) -> TickerPrice:
        return await self.ticker_price_repository.get_last(ticker)

    async def get_ticker_price(self, ticker: Ticker, date: datetime) -> TickerPrice | None:
        ticker_price = await self.ticker_price_repository.get_filtered_by_time(ticker, date)
        
        if ticker_price:
            return ticker_price
        
        return None
