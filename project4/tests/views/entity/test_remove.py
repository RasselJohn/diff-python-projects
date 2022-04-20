from typing import Any, NoReturn

from aiohttp.web_response import Response
from bson import ObjectId
from pymongo import MongoClient

from src.enums import DbCollection


async def test_entity_remove_success(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        user_fx: dict,
        auth_token_fx: dict
):
    login: str = user_fx.get('login')
    entity_id: ObjectId = db_fx[DbCollection.ENTITY].insert_one(
        {'login': login, 'data': {'data1': 123, 'data2': 'qwe'}}
    ).inserted_id

    response: Response = await aiohttp_client_fx.delete(
        aiohttp_client_fx.app.router['entity-remove'].url_for(entity_id=str(entity_id)),
        headers=auth_token_fx,
    )

    assert response.status == 200
    assert 'message' in await response.json()
    assert db_fx[DbCollection.ENTITY].find_one({'_id': entity_id}) is None


async def test_entity_remove_not_owner(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        auth_token_fx: dict
):
    entity_id: ObjectId = db_fx[DbCollection.ENTITY].insert_one({'login': 'some_test_user', 'data': 'qwe'}).inserted_id

    # but auth_token_fx is for other user
    response: Response = await aiohttp_client_fx.delete(
        aiohttp_client_fx.app.router['entity-remove'].url_for(entity_id=str(entity_id)),
        headers=auth_token_fx,
    )

    assert response.status == 400

    data: dict = await response.json()
    assert 'error' in data
    assert data.get('error').endswith('does not exist.')
