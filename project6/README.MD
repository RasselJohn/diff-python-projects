Test project #5
=================
Language: **Python**  
Tools: **Aiohttp, Mongo DB, Pytest, Docker**  
**Examples** of requests are into file `main.http`. 

-------
#### Some assumptions(!):
- Auth token is just uuid4 and must be in 'header' of request: {'token': token_value}
- Passwords saved without encryption.
- Login is unique - so references between tables use it, instead of using DBRef;
- Entity == item.

-------

#### Running:
- Direct way: `python manage.py`
- Docker way: `docker-compose -f deploy/docker-compose.yml up --build`. Url `http://localhost:8000/`


#### Tests
From current dir: `pytest -c config/pytest.ini`.

-------
#### Tables(by default all have `_id` field):
- name: `User`, fields: `login, password`;
- name: `Auth`, fields: `login, token, expire`;
- name: `Entity`(e.g **item**)), fields: `login, data`;
- name: `Link`, fields: `new_owner, entity_id`.
 
