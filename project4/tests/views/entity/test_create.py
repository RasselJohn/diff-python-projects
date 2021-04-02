from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_entity_create_success(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    data = {'data1': 123, 'data2': 'qwe'}
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['entity-create'].url_for(),
        headers=auth_token_fx,
        json=data
    )

    assert response.status == 200
    assert 'message' in await response.json()
    assert db_fx[DbCollection.ENTITY].find({'login': user_fx.get('login')}).count() == 1
    assert db_fx[DbCollection.ENTITY].find_one({'login': user_fx.get('login')}).get('data') == data


async def test_entity_create_unauthorized(aiohttp_client_fx: Any) -> NoReturn:
    response: Response = await aiohttp_client_fx.post(aiohttp_client_fx.app.router['entity-create'].url_for())

    assert response.status == 401

    data: dict = await response.json()
    assert 'error' in data
    assert data.get('error').startswith('Access denied. Perhaps auth token was expired.')
