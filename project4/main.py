import asyncio
from os import environ

from aiohttp import web
from pymongo import database, MongoClient
from motor.motor_asyncio import AsyncIOMotorClient
from src.urls import urls

# main app
app = web.Application()
app.add_routes(urls)
main_loop = asyncio.get_event_loop()

# add global settings
app['MONGO_DB'] = AsyncIOMotorClient(
    environ.get('MONGO_HOST', 'localhost'),
    int(environ.get('MONGO_PORT', 27017)),
    io_loop=main_loop
)['MainDb']
app['TOKEN_EXPIRE'] = int(environ.get('TOKEN_EXPIRE', 5))

web.run_app(app, loop=main_loop)
