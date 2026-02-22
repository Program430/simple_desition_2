from datetime import datetime, timezone
from decimal import Decimal
from pydantic import BaseModel, ConfigDict, Field, field_validator

from src.share.domain.ticker_value_object import Ticker


MAX_CHUNK_SIZE = 50


class BasePydanticModel(BaseModel):
    model_config = ConfigDict(
        from_attributes=True,
        extra='ignore',
        strict=False
    )


class TickerBase(BasePydanticModel):
    ticker: Ticker


class GetAllTickers(TickerBase):
    start_date: datetime = Field(
        default_factory=lambda: datetime.now(tz=timezone.utc),
    )
    limit: int = MAX_CHUNK_SIZE

    @field_validator('start_date', mode='before')
    @classmethod
    def convert_date_to_datetime(cls, value: datetime | int) -> datetime:
        if isinstance(value, (int, str)):
            try:
                return datetime.fromtimestamp(value, timezone.utc)
            except Exception as e:
                raise ValueError(f"Invalid timestamp format: {str(e)}")
            
        return value


class GetFilteredTickerPrice(TickerBase):
    date: datetime


class TickerPriceBase(BasePydanticModel):
    id: int
    ticker: Ticker
    price: Decimal
    created_at: datetime
