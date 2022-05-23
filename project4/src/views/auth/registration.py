from http import HTTPStatus

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorCollection

from src.enums import DbCollection
from src.models import AuthModel
from src.utils import get_password_hash


class RegistrationView(web.View):
    async def post(self) -> web.Response:
        data: AuthModel = await AuthModel.parse_request(self.request)
        login, password = data.login, data.password

        users_collection: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        if await users_collection.find_one({'login': login}):
            return web.json_response(
                {'error': f'User with login={login} already exists.'},
                status=HTTPStatus.BAD_REQUEST
            )

        await users_collection.insert_one({'login': login, 'password': get_password_hash(password.get_secret_value())})
        return web.json_response({'message': 'User was registered successfully!'})
