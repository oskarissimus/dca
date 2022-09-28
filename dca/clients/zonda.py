import datetime as dt
import hmac
import uuid
from decimal import Decimal

import requests

from dca.clients.exchange_client import ExchangeClient
from dca.models.zonda import Symbol, ZondaOfferRequestDTO, ZondaTickerResponseDTO


class ZondaClient(ExchangeClient):  # pylint: disable=too-few-public-methods
    def __init__(self, api_key: str, api_secret: str) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = "https://api.zonda.exchange/rest"

    def buy_market(self, symbol: Symbol, desired_value: Decimal):
        price = self.fetch_price(symbol)
        amount = self.calculate_amount(desired_value, price)

        payload = ZondaOfferRequestDTO.buy_market(amount=amount).json()
        url = f"{self._base_url}/trading/offer/{symbol}"
        response = self._make_request("POST", url, payload)
        return response.text

    def calculate_amount(self, desired_value: Decimal, price: Decimal) -> Decimal:
        return desired_value / price

    def fetch_price(self, symbol: Symbol) -> Decimal:
        url = f"{self._base_url}/trading/ticker/{symbol}"
        response = requests.get(url, timeout=5)
        print(response.text)
        print(symbol.value)
        return ZondaTickerResponseDTO.parse_raw(response.text).ticker.rate

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
