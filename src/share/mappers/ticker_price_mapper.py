from datetime import datetime, timezone

from src.share.database.models.ticker_price_model import TickerPriceModel
from src.share.domain.ticker_price_entity import TickerPrice
from src.share.domain.ticker_value_object import Ticker


class TickerPriceMapper:
    @classmethod
    def to_entity(cls, model: TickerPriceModel) -> TickerPrice:
        return TickerPrice(
            id=model.id,
            ticker=Ticker(model.ticker),
            price=model.price,
            created_at=cls.timestamp_to_datetime(model.created_at)
        )
    
    
    @staticmethod
    def timestamp_to_datetime(timestamp: int) -> datetime:
        return datetime.fromtimestamp(timestamp, tz=timezone.utc)
    
    
    @staticmethod
    def datetime_to_timestamp(date: datetime) -> int:
        return int(date.timestamp())
    
    
    @classmethod
    def to_model(cls, entity: TickerPrice) -> TickerPriceModel:
        model = TickerPriceModel(
            ticker=entity.ticker.value,
            price=entity.price,
        )
        if entity.id is not None:
            model.id = entity.id
        if entity.created_at is not None:
            model.created_at = cls.datetime_to_timestamp(entity.created_at)
            
        return model
