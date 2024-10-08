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
    ETH_PLN = "ETH-PLN"
    LTC_PLN = "LTC-PLN"


class ZondaOfferRequestDTO(BaseModel):
    offerType: OfferType
    amount: Optional[Decimal] = None
    price: Optional[Decimal] = None
    rate: Optional[Decimal] = None
    postOnly: bool
    mode: Mode
    fillOrKill: bool
    immediateOrCancel: bool

    @classmethod
    def buy_market(cls, amount: Decimal):
        return cls(
            offerType=OfferType.BUY.value,
            amount=f"{amount:.8f}",
            mode=Mode.MARKET.value,
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
