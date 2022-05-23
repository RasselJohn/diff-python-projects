from http import HTTPStatus

from aiohttp import web
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection

from src.enums import DbCollection
from src.models.link import LinkModel
from src.utils import require_auth


class GenerateLinkView(web.View):
    @require_auth
    async def post(self) -> web.Response:
        link_item: LinkModel = await LinkModel.parse_request(self.request)
        entity_id, new_owner = link_item.item_id, link_item.new_owner

        users: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.USER]
        if not await users.find_one({'login': new_owner}):
            return web.json_response(
                {'error': f'User with login={new_owner} does not exist.'},
                status=HTTPStatus.BAD_REQUEST
            )

        # before transition to other user - check current user permission on entity
        entities: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        if not await entities.find_one({'_id': ObjectId(entity_id), 'login': self.request.user.get('login')}):
            return web.json_response(
                {'error': f'Item with id={entity_id} does not exist.'},
                status=HTTPStatus.BAD_REQUEST
            )

        links: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.LINK]
        link_id = (await links.insert_one({'new_owner': new_owner, 'entity_id': entity_id})).inserted_id

        url = self.request.app.router['link-receive'].url_for().with_query({'link_id': str(link_id)})
        return web.json_response({'link': f'{self.request.scheme}://{self.request.host}{url}'})
