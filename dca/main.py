import base64

import functions_framework

from dca.clients.xtb.xtb_client_wrapper import XTBClientWrapper
from dca.models.xtb import Message
from dca.settings import Settings


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def kupuj(cloud_event):
    raw_message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    message = Message.parse_raw(raw_message)
    settings = Settings()
    client = XTBClientWrapper(settings.xtb_user_id, settings.xtb_password, settings.xtb_api_port)
    client.buy(message.symbol, message.volume)
