from aiohttp import web
from src.views import auth, entity, link

urls = [
    # auth
    web.post('/registration', auth.RegistrationView, name='registration'),
    web.post('/login', auth.LoginView, name='login'),

    # entity
    web.post('/entity/create', entity.CreateEntityView, name='entity-create'),
    web.get('/entity/list', entity.ListEntitiesView, name='entity-list'),
    web.delete('/entity/remove/{entity_id}', entity.RemoveEntityView, name='entity-remove'),

    # link
    web.post('/link/generate', link.GenerateLinkView, name='link-generate'),
    web.get('/link/receive/', link.ReceiveLinkView, name='link-receive'),
]
