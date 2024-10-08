import datetime as dt
import hmac
import uuid
from decimal import Decimal

import requests

from dca.clients.abstract_exchange_client import AbstractExchangeClient, InvalidSymbolForExchange
from dca.models.zonda import Symbol, ZondaOfferRequestDTO, ZondaTickerResponseDTO


class ZondaClient(AbstractExchangeClient):  # pylint: disable=too-few-public-methods
    def __init__(self, api_key: str, api_secret: str) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = "https://api.zondacrypto.exchange/rest"

    def buy_market(self, symbol: Symbol, desired_value_pln: Decimal):
        if not isinstance(symbol, Symbol):
            raise InvalidSymbolForExchange(
                f"Symbol {symbol} is not supported by {self.__class__.__name__}"
            )
        price = self.fetch_price(symbol)
        amount = self.calculate_amount(desired_value_pln, price)

        payload = ZondaOfferRequestDTO.buy_market(amount=amount).model_dump_json()
        url = f"{self._base_url}/trading/offer/{symbol.value}"
        response = self._make_request("POST", url, payload)
        print(response.text)
        return response.text

    def calculate_amount(self, desired_value: Decimal, price: Decimal) -> Decimal:
        return desired_value / price

    def fetch_price(self, symbol: Symbol) -> Decimal:
        url = f"{self._base_url}/trading/ticker/{symbol.value}"
        response = requests.get(url, timeout=5)
        return ZondaTickerResponseDTO.model_validate_json(response.text).ticker.rate

    def _make_request(self, method: str, url: str, payload: str = "") -> requests.Response:
        current_timestamp = int(dt.datetime.now().timestamp())
        api_hash = self._make_signature(current_timestamp, payload)
        headers = {
            "Content-Type": "application/json",
            "API-Hash": api_hash,
            "API-Key": self._api_key,
            "Request-Timestamp": str(current_timestamp),
            "operation-id": str(uuid.uuid4()),
        }
        response = requests.request(method, url, data=payload, headers=headers, timeout=10)
        return response

    def _make_signature(self, timestamp: int, payload: str) -> str:
        key = self._api_secret.encode("utf-8")
        msg = f"{self._api_key}{timestamp}{payload}".encode("utf-8")
        return hmac.new(key, msg, "SHA512").hexdigest()

    def parse_symbol(self, symbol_str: str) -> Symbol:
        try:
            return Symbol(symbol_str)
        except ValueError as error:
            raise InvalidSymbolForExchange(
                f"Symbol {symbol_str} is not supported by {self.__class__.__name__}"
            ) from error
