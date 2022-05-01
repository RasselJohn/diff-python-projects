import asyncio
from datetime import datetime, timedelta
from os import environ
from typing import Callable, Any
from uuid import uuid4

import pytest
from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from src.enums import DbCollection
from src.urls import urls
from src.utils import get_password_hash


@pytest.fixture(autouse=True)
async def aiohttp_client_fx(aiohttp_client: Callable[[Any], Any], aio_db_fx: AsyncIOMotorDatabase):
    app = web.Application()
    app.add_routes(urls)

    # add global settings
    app['MONGO_DB'] = aio_db_fx
    app['TOKEN_EXPIRE'] = 5

    # use common loop together with mongo db client
    main_loop = aio_db_fx.client.io_loop
    return await aiohttp_client(app, loop=main_loop)


@pytest.fixture
async def aio_db_fx() -> AsyncIOMotorDatabase:
    main_loop: asyncio.AbstractEventLoop = asyncio.get_event_loop()
    db = AsyncIOMotorClient('localhost', 27017, io_loop=main_loop)
    await db.drop_database('MainDb_Test')  # clean db if it exists before
    return db['MainDb_Test']


@pytest.fixture
async def user_fx(aio_db_fx: AsyncIOMotorDatabase) -> dict:
    params_data = {'login': 'test', 'password': get_password_hash('test')}
    await aio_db_fx[DbCollection.USER].insert_one(params_data.copy())
    return {'login': 'test', 'password': 'test'}


@pytest.fixture
async def auth_token_fx(aio_db_fx: AsyncIOMotorDatabase, user_fx: dict) -> dict:
    auth_collection: AsyncIOMotorCollection = aio_db_fx[DbCollection.AUTH]
    login: str = user_fx.get('login')
    token = str(uuid4())

    await auth_collection.replace_one(
        {'login': login},
        {
            'login': login,
            'token': token,
            'expire': datetime.now() + timedelta(10)
        },
        upsert=True
    )

    return {'Authorization': token}
