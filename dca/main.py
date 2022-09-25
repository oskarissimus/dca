import base64

import functions_framework

from dca.models import Symbol
from dca.settings import Settings
from dca.xtb_client_wrapper import XTBClientWrapper


# Triggered from a message on a Cloud Pub/Sub topic.
@functions_framework.cloud_event
def kupuj(cloud_event):
    # Print out the data from Pub/Sub, to prove that it worked
    print(
        "Hello, " + base64.b64decode(cloud_event.data["message"]["data"]).decode() + "!"
    )
    settings = Settings()
    client = XTBClientWrapper(settings.user_id, settings.password)
    client.buy(Symbol.IBTA_UK)
