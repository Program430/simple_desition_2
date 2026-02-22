from datetime import datetime

from sqlalchemy import desc, select, and_
from sqlalchemy.ext.asyncio import AsyncSession

from src.share.database.models.ticker_price_model import TickerPriceModel
from src.share.domain.ticker_price_entity import TickerPrice
from src.share.domain.ticker_value_object import Ticker
from src.share.mappers.ticker_price_mapper import TickerPriceMapper


# Accuracy when try find price ticked by date
ACCURACY = 1


class TickerPriceRepository:
    def __init__(self, session: AsyncSession):
        self._session = session
        
    async def get_chunk(
        self,
        ticker: Ticker,
        start_date: datetime,
        limit: int
    ) -> list[TickerPrice]:
        start_date_timestamp = TickerPriceMapper.datetime_to_timestamp(start_date)
        
        result = await self._session.execute(
            select(TickerPriceModel)
            .where(
                TickerPriceModel.ticker == ticker.value,
                TickerPriceModel.created_at <= start_date_timestamp
            )
            .order_by(desc(TickerPriceModel.created_at))
            .limit(limit)
        )
        
        ticker_price_models = result.scalars().all()
        
        return [TickerPriceMapper.to_entity(ticker_price_model) for ticker_price_model in ticker_price_models]
    
    
    async def get_filtered_by_time(
        self,
        ticker: Ticker,
        date: datetime
    ) -> TickerPrice | None:
        timestamp = TickerPriceMapper.datetime_to_timestamp(date)
        
        result = await self._session.execute(
            select(TickerPriceModel)
            .where(
                and_(
                    TickerPriceModel.ticker == ticker.value,
                    and_(
                        TickerPriceModel.created_at <= timestamp + ACCURACY,
                        TickerPriceModel.created_at >= timestamp - ACCURACY
                    )
                )
            )
            .limit(1)
        )
        
        ticker_price_model = result.scalar_one_or_none()
        
        if ticker_price_model:
            return TickerPriceMapper.to_entity(ticker_price_model)
        
        return None
    
    async def get_last(self, ticker: Ticker) -> TickerPrice:
        result = await self._session.execute(
            select(TickerPriceModel)
            .where(TickerPriceModel.ticker == ticker.value)
            .order_by(desc(TickerPriceModel.created_at))
            .limit(1)
        )
        
        ticker_price_model = result.scalar_one()
        
        return TickerPriceMapper.to_entity(ticker_price_model)

    async def create(self, ticker_price: TickerPrice) -> TickerPrice:
        ticker_price_model = TickerPriceMapper.to_model(ticker_price)
        self._session.add(ticker_price_model)
        await self._session.flush()
        
        return TickerPriceMapper.to_entity(ticker_price_model)
