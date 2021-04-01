Test project #1
=================
Languages: **Python, JS**  
Tools: **Django Framework, Docker**

If local running - firstly there should to create superuser(!): `python manage.py createsuperuser`.  
Running with Docker (in current directory): 
`docker-compose -f deploy/docker-compose.yml up --build`  - project will be by url: http://localhost:8000.

Task:
---------------
- Pages: login + list pages;
- There must be next operations: add/remove/edit user and changing his permissions - full access or only reading access;
- Allowed JS;
- Use ORM and raw sql.