from fastapi import APIRouter, Depends

from src.share.domain.ticker_value_object import Ticker
from src.web.api.api_v1.depends import ticker_price_service_depend
from src.web.api.api_v1.schemas import GetAllTickers, GetFilteredTickerPrice, TickerPriceBase
from src.web.domain.ticker_price_service import TickerPriceService


ticker_price_router = APIRouter(
    prefix='/prices',
    tags=['price']
)


@ticker_price_router.get(
    '',
    response_model=list[TickerPriceBase],
    summary='Get all prices for a ticker',    
)
async def get_all_ticker_prices(
    data: GetAllTickers = Depends(),
    service: TickerPriceService = Depends(ticker_price_service_depend)
) -> list[TickerPriceBase]:
    ticker_prices = await service.get_ticker_price_chunk(
        data.ticker,
        data.start_date,
        data.limit
    )
    
    return [
        TickerPriceBase.model_validate(ticker_price)
        for ticker_price in ticker_prices
    ]


@ticker_price_router.get(
    '/last',
    summary='Get last price for a ticker',    
)
async def get_last_price(
    ticker: Ticker,
    service: TickerPriceService = Depends(ticker_price_service_depend)
) -> TickerPriceBase:
    ticker_price = await service.get_last_ticker_price(ticker)
    
    return TickerPriceBase.model_validate(ticker_price)


@ticker_price_router.get(
    '/filtered',
    summary='Get filtered price for a ticker',    
)
async def get_filtered_price(
    data: GetFilteredTickerPrice = Depends(),
    service: TickerPriceService = Depends(ticker_price_service_depend)
) -> TickerPriceBase | None:
    ticker_price = await service.get_ticker_price(
        data.ticker,
        data.date
    )
    
    if ticker_price:
        return TickerPriceBase.model_validate(ticker_price)
    
    return None
