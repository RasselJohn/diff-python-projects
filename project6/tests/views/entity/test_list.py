from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_entity_list_success(
        db_fx: MongoClient,
        aiohttp_client_fx: Any,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    login: str = user_fx.get('login')
    db_fx[DbCollection.ENTITY].insert_many(
        [{'login': login, 'data': {'data1': 123, 'data2': 'qwe'}} for _ in range(3)]
    )

    response: Response = await aiohttp_client_fx.get(
        aiohttp_client_fx.app.router['entity-list'].url_for(),
        headers=auth_token_fx,
    )

    assert response.status == 200

    data: dict = await response.json()
    assert 'entities' in data
    assert len(data.get('entities')) == 3
