from dca.clients.xtb.x_api_connector import (
    APIClient,
    get_symbol_command,
    login_command,
    trade_transaction_command,
)
from dca.models.xtb import Port, Symbol, SymbolReturnData, TradeTransInfo


class XTBClientWrapper:
    def __init__(self, user_id, password, port: Port):
        self.client = APIClient(port=int(port))
        self.client.execute(login_command(user_id=user_id, password=password))

    def buy(self, symbol: Symbol, volume: int):
        symbol_data = self.get_symbol(symbol)
        ask = symbol_data.ask
        epsilon = 1
        price = ask + epsilon
        trade_trans_info = TradeTransInfo(
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
        return str(self.client.execute(trade_transaction_command(trade_trans_info)))

    def get_symbol(self, symbol: Symbol):
        return SymbolReturnData.parse_obj(
            self.client.execute(get_symbol_command(symbol))["returnData"]
        )
