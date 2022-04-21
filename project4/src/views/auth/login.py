from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Optional
from uuid import uuid4

from motor.motor_asyncio import AsyncIOMotorCollection
from aiohttp import web

from src.enums import DbCollection
from src.utils import get_request_json, check_password_hash


class LoginView(web.View):
    async def post(self) -> web.Response:
        data: Optional[dict] = await get_request_json(self.request)
        if not data:
            return web.json_response(
                {'error': 'Params were not received or had incorrect format.'},
                status=HTTPStatus.UNAUTHORIZED
            )

        login, password = data.get('login'), data.get('password')
        if not login or not password:
            return web.json_response({'error': 'Login or password absent.'}, status=HTTPStatus.UNAUTHORIZED)

        users_collection: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        user: Optional[dict] = await users_collection.find_one({'login': login})
        if not user or not check_password_hash(user.get('password'), password):
            return web.json_response({'error': f'Incorrect auth data.'}, status=HTTPStatus.UNAUTHORIZED)

        # auth token is just uuid4
        token = str(uuid4())
        auth_collection: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.AUTH]
        await auth_collection.replace_one(
            {'login': login},
            {
                'login': login,
                'token': token,
                'expire': datetime.now() + timedelta(minutes=self.request.app.get('TOKEN_EXPIRE'))
            },
            upsert=True
        )

        return web.json_response({'token': token}, status=HTTPStatus.OK)
