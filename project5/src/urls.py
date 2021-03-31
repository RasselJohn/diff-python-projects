from aiohttp import web
from src.views import auth, entity, link

urls = [
    # auth
    web.post('/registration', auth.RegistrationView, name='registration'),
    web.post('/login', auth.LoginView, name='login'),

    # entity (e.g item)
    web.post('/items/new', entity.CreateEntityView, name='entity-create'),
    web.get('/items', entity.ListEntitiesView, name='entity-list'),
    web.delete('/items/{entity_id}', entity.RemoveEntityView, name='entity-remove'),

    # link
    web.post('/send', link.GenerateLinkView, name='link-generate'),
    web.get('/get', link.ReceiveLinkView, name='link-receive'),
]
