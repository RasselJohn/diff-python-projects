from http import HTTPStatus

from aiohttp.web_response import Response

from src.enums import DbCollection


async def test_register_success(aiohttp_client_fx):
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['registration'].url_for(),
        json={'login': 'test_reg', 'password': 'test_reg'}
    )

    assert response.status == HTTPStatus.OK
    assert 'message' in await response.json()
    assert await aiohttp_client_fx.app.get('MONGO_DB')[DbCollection.USER].count_documents({'login': 'test_reg'}) == 1


async def test_register_exist_login(aiohttp_client_fx, user_fx: dict) -> None:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['registration'].url_for(),
        json=user_fx
    )

    assert response.status == HTTPStatus.BAD_REQUEST

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error').endswith('already exists.')


async def test_register_absent_password(aiohttp_client_fx):
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['registration'].url_for(),
        json={'login': 'test'}
    )

    assert response.status == HTTPStatus.BAD_REQUEST

    response_data: dict = await response.json()
    assert isinstance(response_data, list)
    assert len(response_data) == 1
    assert response_data[0]['loc'][0] == 'password'
    assert response_data[0]['msg'] == 'field required'


async def test_register_incorrect_request_data(aiohttp_client_fx):
    response: Response = await aiohttp_client_fx.post(aiohttp_client_fx.app.router['registration'].url_for())

    assert response.status == HTTPStatus.BAD_REQUEST

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error').startswith('Params were not received')
