from http import HTTPStatus
from json.decoder import JSONDecodeError
from typing import Any, Callable, Optional

from aiohttp import web, web_request


# only for class-based views!
def require_auth(class_method: Callable[[Any], Any]) -> Callable[[Any], Any]:
    async def wrapper(*args, **kwargs) -> web.StreamResponse:
        if not args[0].request.user:
            return web.json_response(
                {'error': 'Access denied. Perhaps auth token was expired. Please, log in.'},
                status=HTTPStatus.UNAUTHORIZED
            )

        return await class_method(*args, **kwargs)

    return wrapper


async def get_request_json(request: web_request.Request) -> Optional[dict]:
    try:
        return await request.json()
    except JSONDecodeError:
        return None
