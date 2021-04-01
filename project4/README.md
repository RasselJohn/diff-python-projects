Test project #4
=================
Languages: **Python, JS**  
Tools: **Django Framework, Django Channel**

For running:
```
python manage.py exchange
python manage.py checkadmincurrency
python manage.py runserver
```

Task:
---------------
Create web application for currency exchange.
- There are 2 pages: `/` and `/admin/`
- Page `/` shows current currency exchange rate( Dollar -> Rub).
- App must update exchange rate from third-party sources(http://www.rbc.ru and etc.) silently in extra proccess every 5 minute.
- After update all opened page `/` must be updated with new rate data.
- Page `/admin/` consist of form with 2 fields - `number` and `date`. 
It allows to set custom currency rate before specified `date`, 
e.g real rate will be ignored -  there will be used `number` field value **before** `date`.
- Also page `/admin/` has to show previous values which were printed in the form earlier.
- Allowed to use some UI frameworks on page.
- Allowed to use JS.
- Tests are required.
