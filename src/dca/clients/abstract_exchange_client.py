from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum


class InvalidSymbolForExchange(Exception):
    pass


class AbstractExchangeClient(ABC):
    @abstractmethod
    def buy_market(self, symbol: Enum, desired_value_pln: Decimal):
        pass

    @abstractmethod
    def sell_market(self, symbol: Enum, desired_value_pln: Decimal):
        pass

    @abstractmethod
    def parse_symbol(self, symbol_str: str) -> Enum:
        pass
