import base64

import functions_framework

from dca.clients.exchange_clients import build_exchange_client_by_name
from dca.models.message import Action, Message
from dca.settings import Settings


@functions_framework.cloud_event
def buy_market(cloud_event):
    raw_message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    message = Message.model_validate_json(raw_message)
    settings = Settings()
    client = build_exchange_client_by_name(message.exchange_name, settings=settings)
    symbol = client.parse_symbol(message.symbol)

    if message.action == Action.SELL:
        client.sell_market(symbol, message.desired_value_pln)
    else:
        client.buy_market(symbol, message.desired_value_pln)
