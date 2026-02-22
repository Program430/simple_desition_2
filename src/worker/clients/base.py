from abc import ABC, abstractmethod
from decimal import Decimal

from aiohttp import ClientSession

from src.share.domain.ticker_value_object import Ticker


class PriceClient(ABC):
    def __init__(self, session: ClientSession) -> None:
        ...
        
    @abstractmethod
    async def get_price(self, ticker: Ticker) -> Decimal:
        ...
