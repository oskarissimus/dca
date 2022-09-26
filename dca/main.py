import base64

import functions_framework

from dca.models import Message
from dca.settings import Settings
from dca.xtb_client_wrapper import XTBClientWrapper


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def kupuj(cloud_event):
    raw_message = base64.b64decode(cloud_event.data["message"]["data"]).decode()
    message = Message.parse_raw(raw_message)
    settings = Settings()
    client = XTBClientWrapper(
        settings.user_id, settings.password, settings.xtb_api_port
    )
    client.buy(message.symbol, message.volume)
