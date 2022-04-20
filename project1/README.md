Test project #1
=================

Language: **Python**  
Tools: **Aiohttp Framework, Docker**

Description
---------------

Data loads from current server (3 requests) with waiting period 2 seconds.  

For checking: run `server.py` and open <http://localhost:8080>.  

For checking thorough **Docker** (run in current directory):  `docker-compose -f deploy/docker-compose.yml up --build`

Data will be sorted and printed (in console and main page of site).

Task
---------------

- There are 3 remote sources of data.  
Data is array, where every element consists of `id` and `text` fields.  
Example: 

```json
[  
    {“id”:1, ”name”:”Test 1”}, 
    {“id”:2,”name”:”Test 2”} 
]
```

Access to sources is thorough HTTP.
IDs distribute so :

```json
- first source : ID 1-10,31-40;
- second source: ID 11-20,41-50;
- third source : ID 21-30,51-60;
```

- Only entrypoint(url) exists for getting sorted data.
- The entrypoint must request all sources, get them and sort.
- Errors have to be ignored. Timeout for every source is **2 seconds**.
