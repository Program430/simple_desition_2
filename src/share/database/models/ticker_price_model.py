from decimal import Decimal
from sqlalchemy import Index, Numeric, Integer, String, UniqueConstraint, text
from sqlalchemy.orm import Mapped, mapped_column

from src.share.database.models.base import BaseSqlAlchemyModel


class TickerPriceModel(BaseSqlAlchemyModel):
    __tablename__ = 'ticker_prices'

    id: Mapped[int] = mapped_column(
        Integer, 
        primary_key=True, 
        autoincrement=True
    )
    ticker: Mapped[str] = mapped_column(String(8), nullable=False)
    price: Mapped[Decimal] = mapped_column(Numeric(precision=18, scale=8), nullable=False)
    created_at: Mapped[int] = mapped_column(
        Integer,
        nullable=False,
        server_default=text("extract(epoch from now())::integer")
    )
    
    __table_args__ = (
        UniqueConstraint('ticker', 'created_at', name='uq_ticker_created_at'),
        Index('ix_ticker_created', 'ticker', 'created_at'),
    )
    