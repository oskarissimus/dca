from abc import ABC, abstractmethod
from decimal import Decimal
from enum import Enum


class AbstractExchangeClient(ABC):
    @abstractmethod
    def buy_market(self, symbol: Enum, desired_value_pln: Decimal):
        pass
