import asyncio

import aiohttp
from celery import shared_task

from src.worker.utiles.async_loop_manager import manager
from src.share.database.setup import auto_commit_session
from src.share.domain.ticker_value_object import Ticker
from src.share.core.logger import get_logger
from src.worker.composition.ticker_price_service_composition import ticker_price_service_container
from src.worker.constants import TICKER_PRICE_TASK_NAME


logger = get_logger()


class AddTickerPriceTask:
    @staticmethod
    async def _add_ticker_price(ticker: Ticker) -> None:
        async with aiohttp.ClientSession() as client_session, auto_commit_session() as session:
            ticker_price_service = ticker_price_service_container.get_ticker_price_service(
                client_session=client_session,
                session=session
            )
            
            await ticker_price_service.add_ticker_price(ticker)

    
    @classmethod
    async def add_ticker_prices(cls, tickers: list[Ticker]) -> None:
        add_ticker_prices_coroutines = [
            cls._add_ticker_price(ticker)
            for ticker in tickers
        ]
        
        await asyncio.gather(
            *add_ticker_prices_coroutines,
            return_exceptions=True
        )


@shared_task(name=TICKER_PRICE_TASK_NAME)
def add_ticker_price_task():
    manager.run(
        AddTickerPriceTask.add_ticker_prices(
            [
                Ticker.BTC_USD, 
                Ticker.ETH_USD
            ]
        )
    )
