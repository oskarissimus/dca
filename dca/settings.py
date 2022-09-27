from pydantic import BaseSettings

from dca.models.xtb import Port


class Settings(BaseSettings):
    xtb_user_id: int
    xtb_password: str
    xtb_api_port: Port
    zonda_api_key: str
    zonda_api_secret: str
