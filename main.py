import base64

import functions_framework

from dca.clients.exchange_clients import build_exchange_client_by_name
from dca.models.message import Message
from dca.settings import Settings


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def kupuj(cloud_event):
    raw_message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    message = Message.parse_raw(raw_message)
    settings = Settings()

    client = build_exchange_client_by_name(message.exchange_name, settings=settings)
    symbol = client.parse_symbol(message.symbol)
    client.buy_market(symbol, message.desired_value_pln)
