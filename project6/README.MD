Test project #5
=================
Language: **Python**  
Tools: **Aiohttp, Mongo DB, Pytest, Docker**

### Running:
- Direct way: `python manage.py`
- Docker way: `docker-compose -f deploy/docker-compose.yml up --build`. Url `http://localhost:8000/`
For tests:

### Tests
From current dir: `pytest -c config/pytest.ini`.

Some assumptions(!):
- Auth token is just uuid4.
- Passwords saved without encryption.
- Login is unique - so references between tables use it, instead of using DBRef.

Tables(by default all have `_id` field):
- name: User, fields: login, password;
- name: Auth, fields: login, token, expire;
- name: Entity, fields: login, data;
- name: Link, fields: new_owner, entity_id.
 
