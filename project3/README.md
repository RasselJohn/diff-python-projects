Test project #3
=================

Language: **Python**  
Tools: **Django Framework, Redis, Docker**

For **handle** running:

- Create directory `logs` (path is `LOG_DIR` in `settings.py`)
- Run `Redis`(default settings):
- Run server: `python manage.py runserver`
- For tests (Redis must be running): `python manage.py test`

For running under **Docker** (url: <http://localhost:8000/>):  `docker-compose -f deploy/docker-compose.yml up --build`

**Examples** of API requests is into file **[main.http](main.http)**

Task
---------------

Create web application for simple checking visits of links.

Conditions:

- App has 2 resources (api-urls).
- First resource gets **POST** query with array of visited links and saves it.
Time of visit is getting data by server.
- Second resource gets **GET** query and return unique visited domains for time period.
- Field **status** returns all types of errors or 'ok' if request was success.
- For saving data there was allowed to use only Redis database.
- Tests are required.
