from http import HTTPStatus

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth, get_request_json


# all field in json will be added to 'data' field of entity
class CreateEntityView(web.View):
    @require_auth
    async def post(self) -> web.Response:
        data: dict = await get_request_json(self.request)
        if not data:
            return web.json_response(
                {'error': 'Params were not received or had incorrect format.'},
                status=HTTPStatus.BAD_REQUEST
            )

        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        entities.insert_one({'login': self.request.user.get('login'), 'data': data})

        return web.json_response({'message': 'Item was added successfully!'}, status=HTTPStatus.OK)
