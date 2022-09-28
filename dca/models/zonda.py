from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class OfferType(str, Enum):
    BUY = "BUY"
    SELL = "SELL"


class Mode(str, Enum):
    MARKET = "market"
    LIMIT = "limit"


class Symbol(str, Enum):
    BTC_PLN = "BTC-PLN"


class ZondaOfferRequestDTO(BaseModel):
    offerType: OfferType
    amount: Optional[Decimal]
    price: Optional[Decimal]
    rate: Optional[Decimal]
    postOnly: bool
    mode: Mode
    fillOrKill: bool
    immediateOrCancel: bool

    @classmethod
    def buy_market(cls, amount: Decimal):
        return cls(
            offerType=OfferType.BUY,
            amount=f"{amount:.8f}",
            mode=Mode.MARKET,
            postOnly=False,
            fillOrKill=False,
            immediateOrCancel=False,
        )


class ZondaCurrencyDTO(BaseModel):
    currency: str
    minOffer: Decimal
    scale: int


class ZondaMarketDTO(BaseModel):
    code: str
    first: ZondaCurrencyDTO
    second: ZondaCurrencyDTO
    amountPrecision: int
    pricePrecision: int
    ratePrecision: int


class ZondaTickerDTO(BaseModel):
    market: ZondaMarketDTO
    time: str
    highestBid: Decimal
    lowestAsk: Decimal
    rate: Decimal
    previousRate: Decimal


class ZondaTickerResponseDTO(BaseModel):
    status: str
    ticker: ZondaTickerDTO
