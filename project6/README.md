# Project 6

### Description:

Service has 2 entrypoints:
- '/' - for ws connections
- '/sessions' - for getting all active client_id/sessions 

Nginx connects to 3 containers with load balancing - every new
  connect is on new container - classical nginx strategy - without 'hash_ip' and others.
It can work unstable -
often nginx just throws all connections to first container - 
but balancing can be checked with sending the same client_id in several connections.

Scaling can be reached with addition new containers in docker compose file. 

Ping for ws was added thorough 'uvicorn' settings.

---

### Running

Docker:

```
docker-compose -f deploy/docker-compose.yml -p ws up --build
```
Service will be on `localhost:8400`. 

API docs: `localhost:8400/docs`

---
Clients(examples):

```
python src/client.py --endpoint=ws://localhost:8400 --client-id=test1
python src/client.py --endpoint=ws://localhost:8401 --client-id=test1
python src/client.py --endpoint=ws://localhost:8402 --client-id=test555
```

All connects use one port - nginx proxies on different containers with inner ports - `8880, 8881, 8882`  
