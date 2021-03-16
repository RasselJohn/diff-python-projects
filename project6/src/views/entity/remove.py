from bson.objectid import ObjectId
from http import HTTPStatus

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth


class RemoveEntityView(web.View):
    @require_auth
    async def delete(self) -> web.Response:
        entity_id = ObjectId(self.request.match_info.get('entity_id'))
        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        filter_params = {'_id': entity_id, 'login': self.request.user.get('login')}

        if not entities.find_one(filter_params):
            return web.json_response(
                {'error': f'Entity with id={entity_id} does not exist.'},
                status=HTTPStatus.BAD_REQUEST
            )

        entities.delete_one(filter_params)
        return web.json_response({'message': "Item was removed."}, status=HTTPStatus.OK)
