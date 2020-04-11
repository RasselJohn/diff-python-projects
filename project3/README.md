Test project
=================

- Create virtual environment
- Create dir 'logs' (path is `LOG_DIR` in `settings.py`)
- Run `Redis`(default settings):  
- For handle checking:  
```
python manage.py runserver
```
- For tests (Redis must be running):  
```
python manage.py test
```

Task:
---------------
Create web application for simple checking visits of links.  
Conditions:  
• `Python ~> 3.7`.  
• Application provides JSON API.  
• App has 2 resources(api-urls).  
• First resources gets POST query with array of visited links and saves it. Time of visit is getting data by server.  
• Second resources get GET query and return unique visited domains for time period.  
• Field 'status' returns all types of errors or 'ok' if request was success.  
• For saving data there allowed to use only Redis database.  
• Tests are required.  
