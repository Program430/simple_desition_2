from dataclasses import dataclass
from datetime import datetime
from decimal import Decimal

from src.share.domain.ticker_value_object import Ticker


@dataclass
class TickerPrice:
    ticker: Ticker
    price: Decimal
    id: int | None = None
    created_at: datetime | None = None
