from typing import Any, NoReturn

from aiohttp.web_response import Response
from pymongo import MongoClient

from src.enums import DbCollection


async def test_link_receive_success(
        db_fx: MongoClient,
        aiohttp_client_fx: Any,
        user_fx: dict,
        auth_token_fx: dict
) -> NoReturn:
    # new_owner = 'test_new_owner'
    # db_fx[DbCollection.USER].insert_one({'login': new_owner, 'password': 'qwe'})
    #
    # entity_id = str(db_fx[DbCollection.ENTITY].insert_one({'login': user_fx.get('login'), 'data': {}}).inserted_id)

    response: Response = await aiohttp_client_fx.post(
        aiohttp_client_fx.app.router['link-generate'].url_for(),
        headers=auth_token_fx,
        json={'new_owner': new_owner, 'entity_id': entity_id}
    )

    assert response.status == 200
    assert 'link' in await response.json()
    assert db_fx[DbCollection.LINK].find({'new_owner': new_owner, 'entity_id': entity_id}).count() == 1
