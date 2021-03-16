from http import HTTPStatus

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth


# without pagination
class ListEntitiesView(web.View):
    @require_auth
    async def get(self) -> web.Response:
        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        items = entities.find({'login': self.request.user.get('login')})

        return web.json_response({
            'items': [{
                'id': str(i.get('_id')),
                'data': i.get('data')} for i in items
            ]}, status=HTTPStatus.OK
        )
