from http import HTTPStatus

from aiohttp.web_response import Response
from motor.motor_asyncio import AsyncIOMotorDatabase

from src.enums import DbCollection


async def test_login_success(aiohttp_client_fx, aio_db_fx: AsyncIOMotorDatabase, user_fx: dict):
    response: Response = await aiohttp_client_fx.post(aiohttp_client_fx.app.router['login'].url_for(), json=user_fx)

    assert response.status == HTTPStatus.OK
    assert 'token' in await response.json()
    assert await aio_db_fx[DbCollection.AUTH].count_documents({'login': user_fx.get('login')}) == 1


async def test_login_incorrect_password(aiohttp_client_fx):
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['login'].url_for(),
        json={'login': 'test', 'password': 'test1'}
    )
    assert response.status == HTTPStatus.UNAUTHORIZED

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == 'Incorrect auth data.'


async def test_login_absent_password(aiohttp_client_fx):
    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['login'].url_for(),
        json={'login': 'test'}
    )

    assert response.status == HTTPStatus.UNAUTHORIZED

    response_data: dict = await response.json()
    assert 'error' in response_data
    assert response_data.get('error') == 'Login or password absent.'
