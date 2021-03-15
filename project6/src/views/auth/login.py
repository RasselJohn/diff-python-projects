from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Optional
from uuid import uuid4

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import get_request_json


class LoginView(web.View):
    async def post(self) -> web.Response:
        data: Optional[dict] = await get_request_json(self.request)
        if not data:
            return web.json_response(
                {'error': 'Params were not received or had incorrect format.'},
                status=HTTPStatus.BAD_REQUEST
            )

        login, password = data.get('login'), data.get('password')
        if not login or not password:
            return web.json_response({'error': 'Login or password absent.'}, status=HTTPStatus.BAD_REQUEST)

        users_collection: Collection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        user = users_collection.find_one({'login': login, 'password': password})
        if not user:
            return web.json_response({'error': f'Incorrect auth data.'}, status=HTTPStatus.BAD_REQUEST)

        # auth token is just uuid4
        token = str(uuid4())
        auth_collection: Collection = self.request.app.get('MONGO_DB')[DbCollection.AUTH]
        auth_collection.replace_one(
            {'login': login},
            {
                'login': login,
                'token': token,
                'expire': datetime.now() + timedelta(minutes=self.request.app.get('TOKEN_EXPIRE'))
            },
            upsert=True
        )

        return web.json_response({'token': token}, status=HTTPStatus.OK)
