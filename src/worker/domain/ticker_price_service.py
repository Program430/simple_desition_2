from src.worker.clients.base import PriceClient

from src.share.domain.ticker_price_entity import TickerPrice
from src.share.domain.ticker_value_object import Ticker
from src.share.repository.ticker_price_repository import TickerPriceRepository
from src.share.core.logger import get_logger


logger = get_logger()


class TickerPriceService:
    def __init__(
        self,
        client: PriceClient,
        ticker_price_repository: TickerPriceRepository
    ):
        self._client = client
        self._ticker_price_repository = ticker_price_repository
        
    async def add_ticker_price(self, ticker: Ticker) -> None:
        logger.info(f"Fetch data for ticker={ticker}")
        price = await self._client.get_price(ticker)
        
        ticker_price = TickerPrice(
            ticker=ticker,
            price=price
        )
        
        logger.info("Save data to database")
        await self._ticker_price_repository.create(ticker_price)
        