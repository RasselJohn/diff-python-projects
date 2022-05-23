from http import HTTPStatus

from aiohttp.web_response import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.enums import DbCollection
from src.utils import get_password_hash


async def test_link_generate_success(
        aiohttp_client_fx,
        aio_db_fx: AsyncIOMotorDatabase,
        user_fx: dict,
        auth_token_fx: dict
):
    new_owner = 'test_new_owner'
    await aio_db_fx[DbCollection.USER].insert_one({
        'login': new_owner, 'password': get_password_hash('qwe')
    })

    entity = await aio_db_fx[DbCollection.ENTITY].insert_one({
        'login': user_fx.get('login'), 'data': {}
    })
    entity_id = str(entity.inserted_id)

    request_data = {'new_owner': new_owner, 'item_id': entity_id}
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json=request_data
    )

    assert response.status == HTTPStatus.OK
    assert 'link' in await response.json()
    assert await aio_db_fx[DbCollection.LINK].count_documents({'new_owner': new_owner, 'entity_id': entity_id}) == 1


async def test_link_generate_absent_param(aiohttp_client_fx, auth_token_fx: dict):
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': 'new_owner'}
    )

    assert response.status == HTTPStatus.BAD_REQUEST

    response_data: dict = await response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]['loc'][0] == 'item_id'
    assert response_data[0]['msg'] == 'field required'


async def test_link_generate_absent_user(
        aiohttp_client_fx,
        aio_db_fx: AsyncIOMotorDatabase,
        user_fx: dict,
        auth_token_fx: dict
):
    new_owner = 'absent_user'
    entity = await aio_db_fx[DbCollection.ENTITY].insert_one({
        'login': user_fx.get('login'), 'data': {}
    })
    entity_id = str(entity.inserted_id)

    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': new_owner, 'item_id': entity_id}
    )

    assert response.status == HTTPStatus.BAD_REQUEST

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == f'User with login={new_owner} does not exist.'


async def test_link_generate_has_not_permission_on_entity(
        aiohttp_client_fx,
        aio_db_fx: AsyncIOMotorDatabase,
        auth_token_fx: dict
):
    real_owner = 'real_owner'
    new_owner = 'new_owner'
    entity = await aio_db_fx[DbCollection.ENTITY].insert_one({'login': real_owner, 'data': {}})

    entity_id = str(entity.inserted_id)
    await aio_db_fx[DbCollection.USER].insert_one({'login': new_owner, 'password': 'qwe'})

    # auth_token_fx is token of user, who does not have permissions on the entity
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': new_owner, 'item_id': entity_id}
    )

    assert response.status == HTTPStatus.BAD_REQUEST

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == f'Item with id={entity_id} does not exist.'
