from pydantic import BaseSettings

from dca.models import Port


class Settings(BaseSettings):
    user_id: int
    password: str
    xtb_api_port: Port
