from http import HTTPStatus

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth


class CreateEntityView(web.View):
    @require_auth
    async def post(self) -> web.Response:
        data: dict = await self.request.json()
        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        entities.insert_one({'login': self.request.user.get('login'), 'data': data})
        return web.json_response({'message': 'Entity was added successfully!'}, status=HTTPStatus.OK)
