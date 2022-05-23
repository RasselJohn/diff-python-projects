from pydantic import SecretStr

from src.models.base import BaseRequestModel


class AuthModel(BaseRequestModel):
    login: str
    password: SecretStr
