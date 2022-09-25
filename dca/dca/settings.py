from pydantic import BaseSettings


class Settings(BaseSettings):
    user_id: int
    password: str
