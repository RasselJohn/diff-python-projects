Test project #5
=================

Language: **Python**  
Tools: **Aiohttp, Mongo DB, Pytest, Docker**  

Task
------

Entrypoints:

- `registration/`
- `login/`
- `items/new/` - create item (object with data;  it has a reference to user)
- `items/` -  list of items
- `items/{entity_id}` - remove item
- `send/` -  transfer item to other owner(user)
- `get/` -  receive transfer item by owner

**EXAMPLES(!)** of API requests are in `main.http` file.

Some assumptions
------

- Auth token is just uuid4 and must be in *header* of request: {'Authorization': token_value}
- Login is unique - so references between tables use it, instead of using DBRef.

Running
------

- Straight way: `python manage.py` (**Mongo DB** must be run with default params)
- Docker way: `docker-compose -f deploy/docker-compose.yml up --build`.

After running service will be on `http://localhost:8080/`  

Tests
-------

In current directory: `pytest -c config/pytest.ini`.

Tables
-------

By default all have `_id` field

- name: `User`, fields: `login, password`;
- name: `Auth`, fields: `login, token, expire`;
- name: `Entity`(e.g **item**)), fields: `login, data`;
- name: `Link`, fields: `new_owner, entity_id`.
