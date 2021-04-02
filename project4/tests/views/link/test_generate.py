from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection
from src.utils import get_password_hash


async def test_link_generate_success(
        db_fx: MongoClient,
        aiohttp_client_fx: Any,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    new_owner = 'test_new_owner'
    db_fx[DbCollection.USER].insert_one({'login': new_owner, 'password': get_password_hash('qwe')})
    entity_id = str(db_fx[DbCollection.ENTITY].insert_one({'login': user_fx.get('login'), 'data': {}}).inserted_id)

    request_data = {'new_owner': new_owner, 'item_id': entity_id}
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json=request_data
    )

    assert response.status == 200
    assert 'link' in await response.json()
    assert db_fx[DbCollection.LINK].find({'new_owner': new_owner, 'entity_id': entity_id}).count() == 1


async def test_link_generate_absent_param(aiohttp_client_fx: Any, auth_token_fx: dict) -> NoReturn:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': 'new_owner'}
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error').endswith('params are absent.')


async def test_link_generate_absent_user(
        aiohttp_client_fx: Any,
        db_fx: MongoClient,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    new_owner = 'absent_user'
    entity_id = str(db_fx[DbCollection.ENTITY].insert_one({'login': user_fx.get('login'), 'data': {}}).inserted_id)
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': new_owner, 'item_id': entity_id}
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == f'User with login={new_owner} does not exist.'


async def test_link_generate_has_not_permission_on_entity(
        db_fx: MongoClient,
        aiohttp_client_fx: Any,
        auth_token_fx: dict
) -> NoReturn:
    real_owner = 'real_owner'
    new_owner = 'new_owner'
    entity_id = str(db_fx[DbCollection.ENTITY].insert_one({'login': real_owner, 'data': {}}).inserted_id)
    db_fx[DbCollection.USER].insert_one({'login': new_owner, 'password': 'qwe'})

    # auth_token_fx is token of user, who does not have permissions on the entity
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': new_owner, 'item_id': entity_id}
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == f'Item with id={entity_id} does not exist.'
