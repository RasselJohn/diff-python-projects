from asyncio import ProactorEventLoop
from datetime import datetime, timedelta
from os import environ
from typing import Callable, Any
from uuid import uuid4

import pytest
from _pytest.fixtures import SubRequest
from aiohttp import web
from pymongo import database, MongoClient
from pymongo.collection import Collection

from src.enums import DbCollection
from src.middlewares import check_login
from src.urls import urls


@pytest.fixture  # (scope="session", autouse=True)
def db_fx() -> database.Database:
    client = MongoClient(environ.get('MONGO_HOST', 'localhost'), int(environ.get('MONGO_PORT', 27017)))
    client.drop_database('MainDb_test')
    return client['MainDb_test']


@pytest.fixture
def user_fx(request: SubRequest, db_fx: database.Database) -> dict:
    params_data = {'login': 'test', 'password': 'test'}
    db_fx[DbCollection.USER].insert_one(params_data.copy())

    def remove_user():
        db_fx[DbCollection.USER].delete_one(params_data)

    request.addfinalizer(remove_user)
    return params_data


@pytest.fixture
def auth_token_fx(request: SubRequest, db_fx: database.Database, user_fx: dict) -> dict:
    auth_collection: Collection = db_fx[DbCollection.AUTH]
    login: str = user_fx.get('login')
    token = str(uuid4())

    auth_collection.replace_one(
        {'login': login},
        {
            'login': login,
            'token': token,
            'expire': datetime.now() + timedelta(10)
        },
        upsert=True
    )

    def remove_auth():
        db_fx[DbCollection.AUTH].delete_one({'login': login})

    request.addfinalizer(remove_auth)
    return {'Authorization': token}


@pytest.fixture
def aiohttp_client_fx(db_fx: MongoClient, loop: ProactorEventLoop, aiohttp_client: Callable[[Any], Any]) -> Any:
    app = web.Application()
    app.router.add_routes(urls)
    app.middlewares.append(check_login)

    app['MONGO_DB']: database.Database = db_fx
    app['TOKEN_EXPIRE'] = int(environ.get('TOKEN_EXPIRE', 5))

    return loop.run_until_complete(aiohttp_client(app))
