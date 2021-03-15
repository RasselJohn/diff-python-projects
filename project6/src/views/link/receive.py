from http import HTTPStatus

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth


class ReceiveLinkView(web.View):
    @require_auth
    async def get(self) -> web.Response:
        data = await self.request.json()
        link_id = data.get('link_id')
        if not link_id:
            pass
        new_owner = self.request.user.get('login')
        links: Collection = self.request.app.get('MONGO_DB')[DbCollection.LINK]
        item = links.find_one({'new_owner': new_owner, '_id': link_id})
        if not item:
            pass

        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        entities.update_one(
            {'_id': item.get('entity_id')},
            {'login': new_owner},
            {'upsert': True}
        )

        links.delete_one({'_id': link_id})

        return web.json_response({'message': 'Object was received.'}, status=HTTPStatus.OK)
