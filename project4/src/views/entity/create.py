from http import HTTPStatus

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorCollection

from src.enums import DbCollection
from src.models.item import ItemModel
from src.utils import require_auth


# all field in json will be added to 'data' field of entity
class EntityCreateView(web.View):
    @require_auth
    async def post(self) -> web.Response:
        data = (await ItemModel.parse_request(self.request)).data

        entities: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        await entities.insert_one({'login': self.request.user.get('login'), 'data': data})
        return web.json_response({'message': 'Item was added successfully!'})
