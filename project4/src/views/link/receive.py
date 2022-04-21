from bson import ObjectId
from http import HTTPStatus
from typing import Optional

from aiohttp import web
from motor.motor_asyncio import AsyncIOMotorCollection

from src.enums import DbCollection
from src.utils import require_auth


class ReceiveLinkView(web.View):
    @require_auth
    async def get(self) -> web.Response:
        link_id: Optional[str] = self.request.query.get('link_id')
        if not link_id:
            return web.json_response(
                data={'error': f'Param link_id is absent.'},
                status=HTTPStatus.BAD_REQUEST
            )

        new_owner: str = self.request.user.get('login')
        links: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.LINK]
        link = await links.find_one({'new_owner': new_owner, '_id': ObjectId(link_id)})
        if not link:
            return web.json_response(
                {'error': f'Link with id={link_id} does not exist.'},
                status=HTTPStatus.BAD_REQUEST
            )

        # set new owner for entity
        entities: AsyncIOMotorCollection = self.request.app.get('MONGO_DB')[DbCollection.ENTITY]
        await entities.update_one(
            {'_id': ObjectId(link.get('entity_id'))},
            {'$set': {'login': new_owner}},
            upsert=True
        )

        # remove used link
        await links.delete_one({'_id': ObjectId(link_id)})
        return web.json_response({'message': 'Object was received.'}, status=HTTPStatus.OK)
