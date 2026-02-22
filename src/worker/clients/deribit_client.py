import asyncio
from decimal import Decimal
import logging

from aiohttp import ClientError, ClientResponseError, ClientSession
from tenacity import (
    retry,
    stop_after_attempt,
    retry_if_exception_type,
    before_sleep_log,
    wait_random_exponential
)

from src.worker.domain.exceptions import ParserError, RequestError
from src.share.core.logger import get_logger
from src.worker.clients.base import PriceClient
from src.share.domain.ticker_value_object import Ticker
from src.share.core.config import settings


logger = get_logger()


URL_PREFIX = "/public/get_index_price"
QUERY_TICKER_PARAM = "index_name"
ATTEMPT_COUNT = 3   

class DeribitClient(PriceClient):
    def __init__(self, session: ClientSession):
        self._session = session

    @staticmethod
    def _parse(data: dict) -> Decimal:
        return Decimal(data["result"]["index_price"])
    
    @retry(
        retry=retry_if_exception_type((ClientError, asyncio.TimeoutError)),
        stop=stop_after_attempt(ATTEMPT_COUNT),
        wait=wait_random_exponential(multiplier=1, min=1, max=10),
        before_sleep=before_sleep_log(logger, logging.WARNING)
    )
    async def _get_data(self, ticker: Ticker) -> dict:
        params = {
            QUERY_TICKER_PARAM: ticker.value 
        }
        
        async with self._session.get(
                f"{settings.client_base_url}{URL_PREFIX}", 
                params=params
            ) as response:
                response.raise_for_status()
                return await response.json()
    
    async def get_price(self, ticker: Ticker) -> Decimal:
        try:
           data = await self._get_data(ticker)   
        except ClientResponseError as exc:
            logger.error(
                "Failed get data from Deribit",
                extra={
                    "status_code": exc.status,
                    "error_message": str(exc)
                }
            )
            raise RequestError()
        
        except (asyncio.TimeoutError, ClientError) as exc:
            logger.error(
                "Failed get data from Deribit",
                extra={
                    "error_message": str(exc)
                }
            )
            raise RequestError()

        try:
            return self._parse(data)
        
        except (KeyError, ValueError, TypeError) as exc:
            logger.error(
                "Failed to parse Deribit",
                extra={
                    "data": data,
                    "error_message": str(exc)
                }
            )
            raise ParserError()
            