from decimal import Decimal

from pydantic import BaseModel


class TradeTransInfo(BaseModel):
    cmd: int
    customComment: str
    expiration: int
    offset: int
    order: int
    price: Decimal
    sl: Decimal
    symbol: str
    tp: Decimal
    type: int
    volume: Decimal
