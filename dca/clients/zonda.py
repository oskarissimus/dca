import datetime as dt
import hmac
import uuid
from decimal import Decimal

import requests

from dca.models.zonda import ZondaBuyRequestDTO


class ZondaClient:  # pylint: disable=too-few-public-methods
    def __init__(self, api_key: str, api_secret: str) -> None:
        self._api_key = api_key
        self._api_secret = api_secret
        self._base_url = "https://api.zonda.exchange/rest"

    def buy(self, pair: str, amount: Decimal, price: Decimal):
        payload = ZondaBuyRequestDTO(amount=amount, rate=price).json()
        url = f"{self._base_url}/trading/offer/{pair}"
        response = self._make_request("POST", url, payload)
        return response

    def _make_request(self, method: str, url: str, payload: str = "") -> str:
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
        return response.text

    def _make_signature(self, timestamp: int, payload: str) -> str:
        key = self._api_secret.encode("utf-8")
        msg = f"{self._api_key}{timestamp}{payload}".encode("utf-8")
        return hmac.new(key, msg, "SHA512").hexdigest()
