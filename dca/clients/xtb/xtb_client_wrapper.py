from decimal import Decimal

from dca.clients.exchange_client import ExchangeClient
from dca.clients.xtb.x_api_connector import (
    APIClient,
    get_symbol_command,
    login_command,
    trade_transaction_command,
)
from dca.models.xtb import Port, Symbol, SymbolReturnData, TradeTransInfo


class XTBClientWrapper(ExchangeClient):
    def __init__(self, user_id, password, port: Port):
        self.client = APIClient(port=int(port))
        self.client.execute(login_command(user_id=user_id, password=password))

    def buy_market(self, symbol: Symbol, desired_value_pln: Decimal):
        return self.buy_market_symbol_base_other_than_pln(
            symbol, desired_value_pln, Symbol.USD_PLN
        )

    def buy_market_symbol_base_other_than_pln(
        self, symbol: Symbol, desired_value_pln: Decimal, symbol_for_currency_convertion: Symbol
    ):
        symbol_ask = self.get_symbol_ask(symbol)
        usd_pln_ask = self.get_symbol_ask(symbol_for_currency_convertion)
        volume = self.calculate_volume(usd_pln_ask, symbol_ask, desired_value_pln)
        price = self.calculate_price(symbol_ask)

        trade_trans_info = TradeTransInfo(symbol=symbol, volume=volume, price=price)

        return str(self.client.execute(trade_transaction_command(trade_trans_info)))

    def calculate_volume(
        self, usd_pln_ask: Decimal, symbol_ask: Decimal, desired_value_pln: Decimal
    ):
        return round(desired_value_pln / (usd_pln_ask * symbol_ask))

    def calculate_price(self, price):
        epsilon = 1
        return price + epsilon

    def get_symbol_ask(self, symbol: Symbol):
        return self.get_symbol(symbol).ask

    def get_symbol(self, symbol: Symbol):
        return SymbolReturnData.parse_obj(
            self.client.execute(get_symbol_command(symbol))["returnData"]
        )
