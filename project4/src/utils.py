import hashlib
import os
from datetime import datetime
from http import HTTPStatus
from json.decoder import JSONDecodeError
from typing import Any, Callable, Optional

from aiohttp import web, web_request
from pymongo.collection import Collection

from src.enums import DbCollection


# only for class-based views!
def require_auth(class_method: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(*args, **kwargs) -> web.StreamResponse:
        request = args[0].request
        auth_token: Optional[str] = request.headers.get('Authorization')

        if auth_token:
            # get document by token from db - document also must content user login and token expiration.
            auth_collection: Collection = request.app.get('MONGO_DB')[DbCollection.AUTH]
            authentication_doc: Optional[dict] = auth_collection.find_one({'token': auth_token})

            if authentication_doc:
                if datetime.now() < authentication_doc.get('expire'):
                    request.user = authentication_doc
                    return await class_method(*args, **kwargs)
                else:
                    # expired token must be removed
                    auth_collection.delete_one({'token': auth_token})

        return web.json_response(
            {'error': 'Access denied. Perhaps auth token was expired. Please, log in.'},
            status=HTTPStatus.UNAUTHORIZED
        )

    return wrapper


async def get_request_json(request: web_request.Request) -> Optional[dict]:
    try:
        return await request.json()
    except JSONDecodeError:
        return None


def get_password_hash(password: str, salt_length: int = 32) -> bytes:
    salt = os.urandom(salt_length)
    return salt + hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)


def check_password_hash(password_hash: bytes, password: str, salt_length: int = 32) -> bool:
    return password_hash[salt_length:] == hashlib.pbkdf2_hmac(
        'sha256', password.encode('utf-8'), password_hash[:salt_length], 100000
    )
