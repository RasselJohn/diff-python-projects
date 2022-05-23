from http import HTTPStatus
from typing import Any, NoReturn

from aiohttp.web_response import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.enums import DbCollection


async def test_link_receive_success(
        aiohttp_client_fx: Any,
        aio_db_fx: AsyncIOMotorDatabase,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    old_owner = 'test_old_owner'
    await aio_db_fx[DbCollection.USER].insert_one({'login': old_owner, 'password': 'pass'})

    entity = await aio_db_fx[DbCollection.ENTITY].insert_one({'login': old_owner, 'data': {}})
    entity_id = str(entity.inserted_id)

    link = await aio_db_fx[DbCollection.LINK].insert_one({'new_owner': user_fx.get('login'), 'entity_id': entity_id})
    link_id = str(link.inserted_id)

    response: Response = await aiohttp_client_fx.get(
        aiohttp_client_fx.app.router['link-receive'].url_for().with_query({'link_id': link_id}),
        headers=auth_token_fx,
    )

    assert response.status == HTTPStatus.OK
    assert 'message' in await response.json()
    assert await aio_db_fx[DbCollection.LINK].count_documents(
        {'new_owner': user_fx.get('login'), 'entity_id': entity_id}) == 0
    assert await aio_db_fx[DbCollection.ENTITY].count_documents({'login': old_owner}) == 0
    assert await aio_db_fx[DbCollection.ENTITY].count_documents({'login': user_fx.get('login')}) == 1


async def test_link_receive_no_link(
        aiohttp_client_fx: Any,
        aio_db_fx: AsyncIOMotorDatabase,
        auth_token_fx: dict
) -> NoReturn:
    old_owner = 'test_old_owner'
    entity = await aio_db_fx[DbCollection.ENTITY].insert_one({'login': old_owner, 'data': {}})
    entity_id = str(entity.inserted_id)

    link = await aio_db_fx[DbCollection.LINK].insert_one({'new_owner': old_owner, 'entity_id': entity_id})
    link_id = str(link.inserted_id)

    response: Response = await aiohttp_client_fx.get(
        aiohttp_client_fx.app.router['link-receive'].url_for().with_query({'link_id': link_id}),
        headers=auth_token_fx,
    )

    assert response.status == HTTPStatus.BAD_REQUEST
    data: dict = await response.json()
    assert 'error' in data
    assert data.get('error') == f'Link with id={link_id} does not exist.'
