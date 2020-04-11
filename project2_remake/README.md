Test project #2 REMAKE
=================
Project is on Aiohttp.
Now data is loaded from current server(3 requests) with waiting period 2 seconds.
For checking: run server.py in console and pass to http://localhost:8080.
Data will be sorted and printed (in console and on main page of site).

Task
---------------
- There exist 3 remote sources of data
(for test project these sources can be 2 static json files)
Data is array, where every element consists of id and text field.
Example:
```
[ {“id”:1,”name”:”Test 1”}, {“id”:2,”name”:”Test 2”} ]
```
Access to sources is thorough HTTP.
IDs distribute so :

```
- first source : ID 1-10,31-40;
- second source: ID 11-20,41-50;
- third source : ID 21-30,51-60;
```

- There exist only point(url) for getting these sorted data.

- This point must make request to all sources, gets them and sorts.
- All errors have to be ignored. Timeout for every source - 2 seconds.