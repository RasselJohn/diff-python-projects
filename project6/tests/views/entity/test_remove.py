from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_entity_remove_success(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    # at first delete all data
    db_fx[DbCollection.ENTITY].delete_many({})

    login: str = user_fx.get('login')
    data = {'login': login, 'data': {'data1': 123, 'data2': 'qwe'}}

    # data will receive 'id' field
    db_fx[DbCollection.ENTITY].insert_one(data)
    response: Response = await aiohttp_client_fx.delete(
        aiohttp_client_fx.app.router['entity-remove'].url_for(entity_id=str(data.get('_id'))),
        headers=auth_token_fx,
    )

    assert response.status == 200
    assert 'message' in await response.json()
    assert db_fx[DbCollection.ENTITY].find_one({'_id': data.get('_id')}) is None


async def test_entity_remove_not_owner(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    # at first delete all data
    db_fx[DbCollection.ENTITY].delete_many({})

    owner_login = f'{user_fx.get("login")}_1'
    data = {'login': owner_login, 'data': {'data1': 1243, 'data2': 'qwe'}}
    # data will receive 'id' field
    db_fx[DbCollection.ENTITY].insert_one(data)

    # but auth_token_fx is for other user
    response: Response = await aiohttp_client_fx.delete(
        aiohttp_client_fx.app.router['entity-remove'].url_for(entity_id=str(data.get('_id'))),
        headers=auth_token_fx,
    )

    assert response.status == 400

    data: dict = await response.json()
    assert 'error' in data
    assert data.get('error').endswith('does not exist.')
