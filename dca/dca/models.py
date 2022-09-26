from decimal import Decimal
from enum import Enum
from typing import Optional

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


class Symbol(str, Enum):
    CSPX_UK = "CSPX.UK_9"  # SNP 500
    IBTA_UK = "IBTA.UK"  # USA Bonds


class Currency(str, Enum):
    USD = "USD"


class SymbolReturnData(BaseModel):
    symbol: Symbol
    currency: Currency
    categoryName: str
    currencyProfit: Currency
    quoteId: int
    quoteIdCross: int
    marginMode: int
    profitMode: int
    pipsPrecision: int
    contractSize: int
    exemode: int
    time: int
    expiration: Optional[int]
    stopsLevel: int
    precision: int
    swapType: int
    stepRuleId: int
    type: int
    instantMaxVolume: int
    groupName: str
    description: str
    longOnly: bool
    trailingEnabled: bool
    marginHedgedStrong: bool
    swapEnable: bool
    percentage: Decimal
    bid: Decimal
    ask: Decimal
    high: Decimal
    low: Decimal
    lotMin: Decimal
    lotMax: Decimal
    lotStep: Decimal
    tickSize: Decimal
    tickValue: Decimal
    swapLong: Decimal
    swapShort: Decimal
    leverage: Decimal
    spreadRaw: Decimal
    spreadTable: Decimal
    starting: Optional[int]
    swap_rollover3days: int
    marginMaintenance: int
    marginHedged: int
    initialMargin: int
    timeString: str
    shortSelling: bool
    currencyPair: bool


class Message(BaseModel):
    symbol: Symbol
    volume: int
