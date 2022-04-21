from http import HTTPStatus
from typing import Optional

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorCollection

from src.enums import DbCollection
from src.utils import get_request_json, get_password_hash


class RegistrationView(web.View):
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

        users_collection: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        if await users_collection.find_one({'login': login}):
            return web.json_response(
                {'error': f'User with login={login} already exists.'},
                status=HTTPStatus.BAD_REQUEST
            )

        await users_collection.insert_one({'login': login, 'password': get_password_hash(password)})
        return web.json_response({'message': 'User was registered successfully!'}, status=HTTPStatus.OK)
