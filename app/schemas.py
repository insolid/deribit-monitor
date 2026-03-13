from decimal import Decimal

from pydantic import BaseModel


class Ticker(BaseModel):
    id: int | None = None
    symbol: str
    price: Decimal
    timestamp: int
