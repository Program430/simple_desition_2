from aiohttp import ClientSession
from sqlalchemy.ext.asyncio import AsyncSession

from src.worker.clients.base import PriceClient
from src.worker.clients.deribit_client import DeribitClient
from src.worker.domain.ticker_price_service import TickerPriceService
from src.share.repository.ticker_price_repository import TickerPriceRepository


class TickerPriceServiceContainer:
    def __init__(self, price_client: type[PriceClient]):
        self._price_client = price_client
    
    def _get_client(self, session: ClientSession) -> PriceClient:
        return self._price_client(session)
        
    def _get_repository(self, session: AsyncSession) -> TickerPriceRepository:
        return TickerPriceRepository(session)
        
    def get_ticker_price_service(
        self,
        client_session: ClientSession,
        session: AsyncSession
    ) -> TickerPriceService:
        return TickerPriceService(
            self._get_client(client_session),
            self._get_repository(session)
        )

ticker_price_service_container = TickerPriceServiceContainer(DeribitClient)
