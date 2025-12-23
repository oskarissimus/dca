from enum import Enum as PyEnum
from typing import Union

from pydantic import BaseModel, validator

from dca.clients.exchange_clients import exchange_name_to_builder_mapping
from dca.models.xtb import Symbol as XTBSymbol
from dca.models.zonda import Symbol as ZondaSymbol


class Action(str, PyEnum):
    BUY = "buy"
    SELL = "sell"


class Message(BaseModel):
    exchange_name: str
    symbol: Union[XTBSymbol, ZondaSymbol]
    action: Action = Action.BUY
    desired_value_pln: int

    @validator("exchange_name")
    def exchange_name_is_valid(cls, val):
        if val not in exchange_name_to_builder_mapping:
            raise ValueError(f"Exchange name {val} is not supported")
        return val
