from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum


class ExchangeClient(ABC):
    @abstractmethod
    def buy_market(self, symbol: Enum, desired_value: Decimal):
        pass

    @abstractmethod
    def calculate_amount(self, desired_value: Decimal, price: Decimal) -> Decimal:
        pass
