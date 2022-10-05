from dca.clients.abstract_exchange_client import AbstractExchangeClient
from dca.clients.xtb.xtb_client_wrapper import XTBClientWrapper
from dca.clients.zonda import ZondaClient
from dca.settings import Settings


class ExchangeClientDoesNotExistError(Exception):
    pass


def build_xtb_client(settings: Settings) -> XTBClientWrapper:
    return XTBClientWrapper(
        user_id=settings.xtb_user_id, password=settings.xtb_password, port=settings.xtb_api_port
    )


def build_zonda_client(settings: Settings) -> ZondaClient:
    return ZondaClient(api_key=settings.zonda_api_key, api_secret=settings.zonda_api_secret)


exchange_name_to_builder_mapping = {"xtb": build_xtb_client, "zonda": build_zonda_client}


def build_exchange_client_by_name(
    exchange_name: str, settings: Settings
) -> AbstractExchangeClient:
    if exchange_name not in exchange_name_to_builder_mapping:
        raise ExchangeClientDoesNotExistError(
            f"Exchange client for {exchange_name} does not exist"
        )
    return exchange_name_to_builder_mapping[exchange_name](settings)
