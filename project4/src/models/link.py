from src.models.base import BaseRequestModel


class LinkModel(BaseRequestModel):
    item_id: str
    new_owner: str
