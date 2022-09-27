from decimal import Decimal

from pydantic import BaseModel


class ZondaBuyRequestDTO(BaseModel):
    amount: Decimal
    rate: Decimal
    offerType: str = "buy"
    mode: str = "limit"
    postOnly: bool = False
    fillOrKill: bool = False
