from dca.models import Symbol, SymbolReturnData, TradeTransInfo
from dca.xAPIConnector import (
    APIClient,
    getSymbolCommand,
    loginCommand,
    tradeTransactionCommand,
)


class XTBClientWrapper:
    def __init__(self, user_id, password):
        self.client = APIClient()
        self.client.execute(loginCommand(userId=user_id, password=password))

    def buy(self, symbol: Symbol, volume: int):
        symbol_data = self.get_symbol(symbol)
        ask = symbol_data.ask
        epsilon = 1
        price = ask + epsilon
        t = TradeTransInfo(
            cmd=0,
            customComment="",
            expiration=0,
            offset=0,
            order=0,
            price=price,
            sl=0,
            symbol=symbol.value,
            tp=0,
            type=0,
            volume=volume,
        )
        return str(self.client.execute(tradeTransactionCommand(t)))

    def get_symbol(self, symbol: Symbol):
        return SymbolReturnData.parse_obj(
            self.client.execute(getSymbolCommand(symbol))["returnData"]
        )
