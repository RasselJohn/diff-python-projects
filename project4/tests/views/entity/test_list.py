from http import HTTPStatus
from typing import Any

from aiohttp.web_response import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.enums import DbCollection


async def test_entity_list_success(
        aio_db_fx: AsyncIOMotorDatabase,
        aiohttp_client_fx: Any,
        user_fx: dict,
        auth_token_fx: dict
):
    login: str = user_fx.get('login')
    await aio_db_fx[DbCollection.ENTITY].insert_many(
        [{'login': login, 'data': {'data1': 123, 'data2': 'qwe'}} for _ in range(3)]
    )

    response: Response = await aiohttp_client_fx.get(
        aiohttp_client_fx.app.router['entity-list'].url_for(),
        headers=auth_token_fx,
    )

    assert response.status == HTTPStatus.OK

    data: dict = await response.json()
    assert 'items' in data
    assert len(data.get('items')) == 3
