Test project #3
=================

Language: **Python**  
Tools: **Django Framework, Redis, Docker**

Running
---------------
Service will be on url: <http://localhost:8000/>

**Local:**
- Create directory `logs` (path is `LOG_DIR` in `settings.py`)
- Run `Redis`(default settings):
- Run server: `python manage.py runserver`
- For tests (Redis must be running): `python manage.py test`

**Docker:**  
 `docker-compose -f deploy/docker-compose.yml up --build`

**Examples** of API requests are in file **[main.http](main.http)**

Task
---------------

Create web application for simple checking visits of links.

- App has 2 entrypoints.
- First url gets **POST** query with array of visited links and saves it. Server saves time of visit.
- Second url gets **GET** query and return unique visited domains for time period.
- Field **status** keeps errors or 'ok' if request was success.
- For saving data only Redis may be used.
- Tests are required.
