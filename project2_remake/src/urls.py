from aiohttp import web
from src.apps.frontend import views

urls = [
    web.get('/', views.IndexView, name='index'),
    web.get('/remote', views.RemoteView, name='remote')
]
