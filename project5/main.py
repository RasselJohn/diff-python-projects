from os import environ

from aiohttp import web
from pymongo import database, MongoClient

from src.middlewares import check_login
from src.urls import urls

# main app
app = web.Application()
app.add_routes(urls)
app.middlewares.append(check_login)

# add global setting - advice from official documentation!
app['MONGO_DB']: database.Database = MongoClient(
    environ.get('MONGO_HOST', 'localhost'), int(environ.get('MONGO_PORT', 27017))
)['MainDb']
app['TOKEN_EXPIRE'] = int(environ.get('TOKEN_EXPIRE', 5))

web.run_app(app)
