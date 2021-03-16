from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_login_success(aiohttp_client_fx: Any, db_fx: MongoClient, user_fx: dict) -> NoReturn:
    response: Response = await aiohttp_client_fx.post(aiohttp_client_fx.app.router['login'].url_for(), json=user_fx)

    assert response.status == 200
    assert 'token' in await response.json()
    assert db_fx[DbCollection.AUTH].find({'login': user_fx.get('login')}).count() == 1


async def test_login_incorrect_password(aiohttp_client_fx: Any) -> NoReturn:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['login'].url_for(),
        json={'login': 'test', 'password': 'test1'}
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == 'Incorrect auth data.'


async def test_login_absent_password(aiohttp_client_fx: Any) -> None:
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['login'].url_for(),
        json={'login': 'test'}
    )

    assert response.status == 400

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == 'Login or password absent.'
