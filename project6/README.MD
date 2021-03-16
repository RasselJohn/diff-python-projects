Test project #6
=================
Language: **Python**  
Tools: **Aiohttp, Mongo DB, Pytest, Docker**

For running:
- Direct way: `python manage.py`
- Docker way: `docker-compose -f deploy/docker-compose.yml up --build`. Url `http://localhost:8000/`

Some assumptions(!):
- Auth token is just uuid4.
- Passwords saved without encryption.
- Login is unique - so references between tables use it, instead of using DBRef.

Tables(by default all have `_id` field):
- name: User, fields: login, password 
- name: Auth, fields: login, token, expire
- name: Entity, fields: login, data.
- name: Link, fields: entity_id, new_owner.
 
