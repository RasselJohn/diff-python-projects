from http import HTTPStatus

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth


class GenerateLinkView(web.View):
    @require_auth
    async def post(self) -> web.Response:
        data = await self.request.json()
        entity_id: int = data.get('entity_id')
        owner: int = data.get('owner')
        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        filter_params = {'_id': entity_id, 'login': self.request.user.get('login')}

        if not entity_id or entities.find_one(filter_params):
            return web.json_response(
                {'error': f'Entity with id={entity_id} does not exist'},
                status=HTTPStatus.BAD_REQUEST
            )

        links: Collection = self.request.app.get('MONGO_DB')[DbCollection.LINK]
        item = links.insert_one({'new_owner': owner, 'entity_id': entity_id})

        url = str(self.request.app.router['root'].url_for().with_query({'link_id': item._id}))
        return web.json_response({'link': url}, status=HTTPStatus.OK)
