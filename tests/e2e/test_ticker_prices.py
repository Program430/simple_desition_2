import pytest
from datetime import datetime, timezone
from httpx import AsyncClient
from fastapi import status

from tests.constants import ETH, BTC


URL_PREFIX = "/prices"


@pytest.mark.parametrize(
    "ticker,start_date,limit",
    [
        (ETH, int(datetime.now(tz=timezone.utc).timestamp()), 5),
        (ETH, datetime.now(tz=timezone.utc), 5),
        (BTC, int(datetime.now(tz=timezone.utc).timestamp()), 5),
        (BTC, datetime.now(tz=timezone.utc), 2),
    ]
)
@pytest.mark.asyncio
async def test_get_all_ticker_prices__with_valid_data__return_limited_count(
    client: AsyncClient,
    ticker: str,
    start_date: datetime | int,
    limit: int
):
    params = {
        "ticker": ticker,
        "start_date": start_date,
        "limit": limit
    }
    
    response = await client.get(URL_PREFIX, params=params)
    
    assert response.status_code == status.HTTP_200_OK
    
    price_tickers = response.json()
    
    assert len(price_tickers) == limit
    