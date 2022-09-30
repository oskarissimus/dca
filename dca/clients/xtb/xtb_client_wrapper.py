from decimal import Decimal

from dca.clients.abstract_exchange_client import AbstractExchangeClient, InvalidSymbolForExchange
from dca.clients.xtb.x_api_connector import (
    APIClient,
    get_symbol_command,
    login_command,
    trade_transaction_command,
)
from dca.models.xtb import Currency, Port, Symbol, SymbolReturnData, TradeTransInfo


class XTBClientWrapper(AbstractExchangeClient):  # pylint: disable=too-few-public-methods
    def __init__(self, user_id, password, port: Port):
        self.client = APIClient(port=int(port))
        self.client.execute(login_command(user_id=user_id, password=password))

    def buy_market(self, symbol: Symbol, desired_value_pln: Decimal):
        symbol_data = self._get_symbol(symbol)
        asset_base_currency = symbol_data.currency
        asset_price = symbol_data.ask
        volume = self._calculate_volume_for_desired_value(
            asset_base_currency, desired_value_pln, asset_price
        )

        price = self._calculate_price(asset_price)
        trade_trans_info = TradeTransInfo(symbol=symbol, volume=volume, price=price)
        return str(self.client.execute(trade_transaction_command(trade_trans_info)))

    def _calculate_volume_for_desired_value(
        self, asset_base_currency: Currency, desired_value_pln: Decimal, asset_price: Decimal
    ):
        asset_price_in_pln = self._calculate_asset_price_in_pln(asset_price, asset_base_currency)
        return desired_value_pln / asset_price_in_pln

    def _calculate_asset_price_in_pln(self, asset_price: Decimal, asset_base_currency: Currency):
        if asset_base_currency == Currency.PLN:
            return asset_price
        if asset_base_currency == Currency.USD:
            return asset_price * self._get_symbol_ask(Symbol.USD_PLN)
        raise Exception("Unsupported currency")

    def _calculate_volume(
        self, usd_pln_ask: Decimal, symbol_ask: Decimal, desired_value_pln: Decimal
    ):
        return round(desired_value_pln / (usd_pln_ask * symbol_ask))

    def _calculate_price(self, price):
        epsilon = 1
        return price + epsilon

    def _get_symbol_ask(self, symbol: Symbol):
        return self._get_symbol(symbol).ask

    def _get_symbol(self, symbol: Symbol):
        return SymbolReturnData.parse_obj(
            self.client.execute(get_symbol_command(symbol))["returnData"]
        )

    def parse_symbol(self, symbol_str: str) -> Symbol:
        try:
            return Symbol(symbol_str)
        except ValueError as error:
            raise InvalidSymbolForExchange(
                f"Symbol {symbol_str} is not supported by {self.__class__.__name__}"
            ) from error
