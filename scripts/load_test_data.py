from decimal import Decimal
import json
import asyncio
from typing import Any

from sqlalchemy import insert
from sqlalchemy.ext.asyncio import AsyncEngine

from src.share.database.models.ticker_price_model import TickerPriceModel
from src.share.database.setup import engine

     
def get_data_from_file(file: str) -> list[dict[str, Any]]:
    ticker_prices = []
    with open(file, encoding="UTF-8") as f:
        for json_line in f:
            if json_line == "\n":
                continue
            
            ticker_price_data = json.loads(json_line, parse_float=Decimal)

            ticker_price = {
                "id": ticker_price_data["id"],
                "ticker": ticker_price_data["ticker"],
                "price": ticker_price_data["price"],
                "created_at": ticker_price_data["created_at"],
            }
            
            ticker_prices.append(ticker_price)
            
        return ticker_prices
            
            
async def load_data_to_database(file: str, engine: AsyncEngine) -> None:
    ticker_prices = get_data_from_file(file)

    async with engine.begin() as conn:
        await conn.execute(insert(TickerPriceModel), ticker_prices)


if __name__ == "__main__":
    asyncio.run(load_data_to_database("tests/data/ticker_prices.jsonl", engine))
