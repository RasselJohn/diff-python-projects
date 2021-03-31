from datetime import datetime
from typing import Any, Optional

from aiohttp import web
from pymongo.collection import Collection

from src.enums import DbCollection


@web.middleware
async def check_login(request: web.Request, handler: Any) -> web.StreamResponse:
    # an anonymous by default
    request.user = None

    auth_token: Optional[str] = request.headers.get('Authorization')
    if auth_token:

        # get document by token from db - document also must content user login and token expiration.
        auth_collection: Collection = request.app.get('MONGO_DB')[DbCollection.AUTH]
        authentication_doc: Optional[dict] = auth_collection.find_one({'token': auth_token})

        if authentication_doc:
            if datetime.now() < authentication_doc.get('expire'):
                request.user = authentication_doc
            else:
                # expired token must be removed
                auth_collection.delete_one({'token': auth_token})

    return await handler(request)
