import json
from http import HTTPStatus
from typing import TypeVar

from aiohttp import web
from aiohttp.web_request import Request
from pydantic import BaseModel, ValidationError

TypeBaseRequestModel = TypeVar('TypeBaseRequestModel', bound='BaseRequestModel')


class BaseRequestModel(BaseModel):
    @classmethod
    async def parse_request(cls, request: Request, *, error_status_code=HTTPStatus.BAD_REQUEST) -> TypeBaseRequestModel:
        try:
            obj = cls.parse_obj(await request.json())

        except ValidationError as e:
            raise web.HTTPBadRequest(body=e.json(), content_type='application/json')

        except Exception as e:
            print("Error", e)
            raise web.HTTPBadRequest(
                body=json.dumps({'error': 'Params were not received or had incorrect format.'}),
                content_type='application/json'
            )

        return obj
