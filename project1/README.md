Test project #1
=================

Languages: **Python, JS**  
Tools: **Django Framework, Docker**

**WARNING!**
This project is not for production! It's just example! Don't use it - or only your responsibility.

---
**Running:**

Project will be by url: <http://localhost:8000>.  
Superuser login: **admin**, password: **admin**.

**Local:**

- Migrate db:  
```python manage.py migrate```

- Add fixtures with superuser auth data:  
```python manage.py loaddata fixtures.json```

- Run server:
```python manage.py runserver 0.0.0.0:8000```

**Docker:**

```docker-compose -f deploy/docker-compose.yml up --build```  

---
Task
---------------

- Pages: login + list of users pages;
- Operations: add/remove/edit user and changing his permissions - full access or only reading access;
- Use JS;
- Use ORM and raw SQL.
