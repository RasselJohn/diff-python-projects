from aiohttp import web
from src.views import auth, entity

urls = [
    # auth
    web.post('/registration', auth.RegistrationView, name='registration'),
    web.post('/login', auth.LoginView, name='login'),

    # entity
    web.post('/entity/create', entity.CreateEntityView, name='entity-create'),
    web.get('/entity/list', entity.ListEntitiesView, name='entity-list'),
    web.delete('/entity/remove/{entity_id}', entity.RemoveEntityView, name='entity-remove'),


]
