from http import HTTPStatus

from aiohttp import web
from bson import ObjectId
from pymongo.collection import Collection

from src.enums import DbCollection
from src.utils import require_auth


class GenerateLinkView(web.View):
    @require_auth
    async def post(self) -> web.Response:
        data: dict = await self.request.json()

        entity_id: str = data.get('entity_id')
        new_owner: int = data.get('new_owner')
        if not entity_id or not new_owner:
            return web.json_response(
                data={'error': f'Entity_id or new_owner params are absent.'},
                status=HTTPStatus.BAD_REQUEST
            )

        users: Collection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        if not users.find_one({'login': new_owner}):
            return web.json_response(
                {'error': f'User with login={new_owner} does not exist.'},
                status=HTTPStatus.BAD_REQUEST
            )

        # before transition to other user - check current user permission on entity
        entities: Collection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        if not entities.find_one({'_id': ObjectId(entity_id), 'login': self.request.user.get('login')}):
            return web.json_response(
                {'error': f'Entity with id={entity_id} does not exist.'},
                status=HTTPStatus.BAD_REQUEST
            )

        links: Collection = self.request.app.get('MONGO_DB')[DbCollection.LINK]
        item = links.insert_one({'new_owner': new_owner, 'entity_id': entity_id})
        url = str(self.request.app.router['link-receive'].url_for().with_query({'link_id': str(item.inserted_id)}))
        return web.json_response({'link': f'{self.request.scheme}://{self.request.host}{url}'}, status=HTTPStatus.OK)
