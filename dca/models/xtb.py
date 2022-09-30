from decimal import Decimal
from enum import Enum
from typing import Optional

from pydantic import BaseModel


class Symbol(str, Enum):
    CSPX_UK = "CSPX.UK_9"  # SNP 500
    IBTA_UK = "IBTA.UK"  # USA Bonds
    USD_PLN = "USDPLN"


class Port(str, Enum):
    DEMO = "5124"
    REAL = "5112"


class Currency(str, Enum):
    USD = "USD"
    PLN = "PLN"


class Cmd(int, Enum):
    BUY = 0
    SELL = 1
    BUY_LIMIT = 2
    SELL_LIMIT = 3
    BUY_STOP = 4
    SELL_STOP = 5
    BALANCE = 6
    CREDIT = 7


class Type(int, Enum):
    OPEN = 0
    PENDING = 1
    CLOSE = 2
    MODIFY = 3
    DELETE = 4


class TradeTransInfo(BaseModel):
    cmd: Cmd = Cmd.BUY
    customComment: str = ""
    expiration: int = 0
    offset: int = 0
    order: int = 0
    price: Decimal
    sl: Decimal = Decimal(0)
    symbol: Symbol
    tp: Decimal = Decimal(0)
    type: Type = Type.OPEN
    volume: Decimal


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
