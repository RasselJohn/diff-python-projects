Test project #5
=================
Language: **Rust**  
Tools: **Actix Framework, Docker**

There was used https://weatherapi.com/ - it requires an API-key.  
For running Docker(API-key should set in compose-file(!)): `docker build -f deploy/docker/Dockerfile -t temperature .`  
In this case service will work on http://localhost:8080/.  

Task:
---------------
Create web application for getting temperature.
- API must have 2 entrypoints.
- First url have to return temperature for concrete city and date (today or in future). 
- Second url have to return array of temperatures for concrete city for week.

