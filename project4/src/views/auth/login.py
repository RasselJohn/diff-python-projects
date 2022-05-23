from datetime import datetime, timedelta
from http import HTTPStatus
from typing import Optional
from uuid import uuid4

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorCollection

from src.enums import DbCollection
from src.models import AuthModel
from src.utils import check_password_hash


class LoginView(web.View):
    async def post(self) -> web.Response:
        data: AuthModel = await AuthModel.parse_request(self.request)
        login, password = data.login, data.password

        users_collection: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        user: Optional[dict] = await users_collection.find_one({'login': login})
        if not user or not check_password_hash(user.get('password'), password.get_secret_value()):
            return web.json_response({'error': 'Incorrect auth data.'}, status=HTTPStatus.UNAUTHORIZED)

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

        return web.json_response({'token': token})
