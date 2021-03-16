from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_link_receive_success(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    old_owner = 'test_old_owner'
    db_fx[DbCollection.USER].insert_one({'login': old_owner, 'password': 'pass'})
    entity_id = str(db_fx[DbCollection.ENTITY].insert_one({'login': old_owner, 'data': {}}).inserted_id)
    link_id = str(
        db_fx[DbCollection.LINK].insert_one({'new_owner': user_fx.get('login'), 'entity_id': entity_id}).inserted_id
    )

    response: Response = await aiohttp_client_fx.get(
        aiohttp_client_fx.app.router['link-receive'].url_for().with_query({'link_id': link_id}),
        headers=auth_token_fx,
    )

    assert response.status == 200
    assert 'message' in await response.json()
    assert db_fx[DbCollection.LINK].find({'new_owner': user_fx.get('login'), 'entity_id': entity_id}).count() == 0
    assert db_fx[DbCollection.ENTITY].find({'login': old_owner}).count() == 0
    assert db_fx[DbCollection.ENTITY].find({'login': user_fx.get('login')}).count() == 1


async def test_link_receive_no_link(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        auth_token_fx: dict
) -> NoReturn:
    old_owner = 'test_old_owner'
    entity_id = str(db_fx[DbCollection.ENTITY].insert_one({'login': old_owner, 'data': {}}).inserted_id)
    link_id = str(
        db_fx[DbCollection.LINK].insert_one({'new_owner': old_owner, 'entity_id': entity_id}).inserted_id
    )

    response: Response = await aiohttp_client_fx.get(
        aiohttp_client_fx.app.router['link-receive'].url_for().with_query({'link_id': link_id}),
        headers=auth_token_fx,
    )

    assert response.status == 400
    data: dict = await response.json()
    assert 'error' in data
    assert data.get('error') == f'Link with id={link_id} does not exist.'
