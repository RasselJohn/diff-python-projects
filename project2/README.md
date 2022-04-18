Test project #2
=================

Language: **Python**  
Tools: **Aiohttp Framework, Docker**

Data loads from current server (3 requests) with waiting period 2 seconds.  

For checking: run server.py in console and **open in browser by address <http://localhost:8080>**.  

For checking thorough **Docker** (run in current directory):  `docker-compose -f deploy/docker-compose.yml up --build`

Data will be sorted and printed (in console and on main page of site).

Task
---------------

- There exist 3 remote sources of data
Data is array, where every element consists of id and text field.
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

- Only point(url) exists for getting sorted data.
- This point must make requests to all sources, to get them and to sort.
- All errors have to be ignored. Timeout for every source - 2 seconds.
- For randomness remote entrypoint can asleep - it allows to break request to it and check the API works correctly.
