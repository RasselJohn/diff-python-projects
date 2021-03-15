from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_register_success(aiohttp_client_fx: Any, db_fx: MongoClient) -> NoReturn:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['registration'].url_for(),
        json={'login': 'test_reg', 'password': 'test_reg'}
    )

    assert response.status == 200
    assert 'message' in await response.json()
    assert db_fx[DbCollection.USER].find({'login': 'test_reg'}).count() == 1


async def test_register_exist_login(aiohttp_client_fx: Any, user_fx: dict) -> None:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['registration'].url_for(),
        json=user_fx
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error').endswith('already exists.')


async def test_register_absent_password(aiohttp_client_fx: Any) -> None:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['registration'].url_for(),
        json={'login': 'test'}
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == 'Login or password absent.'


async def test_register_incorrect_request_data(aiohttp_client_fx: Any) -> None:
    response: Response = await aiohttp_client_fx.post(aiohttp_client_fx.app.router['registration'].url_for())

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error').startswith('Params were not received')
