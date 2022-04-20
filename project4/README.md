Test project #5
=================

Language: **Python**  
Tools: **Aiohttp, Mongo DB, Pytest, Docker**  

**WARNING!**
This project is not for production! It's just example! Don't use it - or only your responsibility.

Task
------

EntryPoints:

- `registration/`
- `login/`
- `items/new/` - create item (object with data;  it has reference to user)
- `items/` -  list of items
- `items/{entity_id}` - remove item
- `send/` -  transfer item to other owner(user)
- `get/` -  receive transfer item by owner

**EXAMPLES(!)** for requests to API are into file `main.http`.

-------

#### Some assumptions(!)

- Auth token is just uuid4 and must be in 'header' of request: {'Authorization': token_value}
- Login is unique - so references between tables use it, instead of using DBRef.

-------

#### Running

- Direct way: `python manage.py`
- Docker way: `docker-compose -f deploy/docker-compose.yml up --build`.

After running (any of ways) service will be on `http://localhost:8080/`  

#### Tests

From current directory: `pytest -c config/pytest.ini`.

-------

#### Tables(by default all have `_id` field)

- name: `User`, fields: `login, password`;
- name: `Auth`, fields: `login, token, expire`;
- name: `Entity`(e.g **item**)), fields: `login, data`;
- name: `Link`, fields: `new_owner, entity_id`.
