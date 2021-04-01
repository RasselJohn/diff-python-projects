from aiohttp import web

from src.urls import urls

app = web.Application()
app.add_routes(urls)
web.run_app(app)
