Set up docker containers
```
docker-compose build
docker-compose up -d
```

Check docker network configuration
```
docker network inspect chronos_default
```

Start services on server
```
docker exec chronos-server-1 bash "setup_service.sh"
```

Create superuser in client app
```
docker exec -it chronos-client-1 python "manage.py createsuperuser"
```

### SSL authentication

Create self-signed (password-less) certificates with
```
openssl req -newkey rsa:2048 -keyout client.key -x509 -days 365 -out client.crt -nodes
openssl req -newkey rsa:2048 -keyout server.key -x509 -days 365 -out server.crt -nodes
```

**FIXES**
When encountering an Authentication failure:  
`ssl.SSLError: [SSL: TLSV1_ALERT_PROTOCOL_VERSION] tlsv1 alert protocol version (_ssl.c:1091)` 

The server is not accepting the protocol TLS_v1_1. Ensure the argument

```
ssl_version=ssl.PROTOCOL_TLSv1_2
```

is passed in the client-side call `rpyc.ssl_connect()`
