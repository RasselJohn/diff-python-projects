from http import HTTPStatus

from aiohttp.web_response import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.enums import DbCollection


async def test_entity_create_success(
        aiohttp_client_fx,
        aio_db_fx: AsyncIOMotorDatabase,
        user_fx: dict,
        auth_token_fx: dict
):
    data = {'data': {'data1': 123, 'data2': 'qwe'}}
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['entity-create'].url_for(),
        headers=auth_token_fx,
        json=data
    )

    assert response.status == HTTPStatus.OK
    assert 'message' in await response.json()
    assert await aio_db_fx[DbCollection.ENTITY].count_documents({'login': user_fx.get('login')}) == 1

    item = await aio_db_fx[DbCollection.ENTITY].find_one({'login': user_fx.get('login')})
    assert item.get('data') == data['data']


async def test_entity_create_unauthorized(aiohttp_client_fx):
    response: Response = await aiohttp_client_fx.post(aiohttp_client_fx.app.router['entity-create'].url_for())

    assert response.status == HTTPStatus.UNAUTHORIZED

    data: dict = await response.json()
    assert 'error' in data
    assert data.get('error').startswith('Access denied. Perhaps auth token was expired.')
