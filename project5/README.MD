Test project #5
=================
Language: **Python**  
Tools: **Aiohttp, Mongo DB, Pytest, Docker**  


-------
#### Some assumptions(!):
- Auth token is just uuid4 and must be in 'header' of request: {'token': token_value}
- Passwords save without encryption;
- Login is unique - so references between tables use it, instead of using DBRef.

-------

#### Running:
- Direct way: `python manage.py`
- Docker way: `docker-compose -f deploy/docker-compose.yml up --build`. 

After running (any of ways) service will be on `http://localhost:8080/`  

**EXAMPLES(!)** for requests to API are into file `main.http`. 

#### Tests
From current directory: `pytest -c config/pytest.ini`.

-------
#### Tables(by default all have `_id` field):
- name: `User`, fields: `login, password`;
- name: `Auth`, fields: `login, token, expire`;
- name: `Entity`(e.g **item**)), fields: `login, data`;
- name: `Link`, fields: `new_owner, entity_id`.
 
