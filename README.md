# BetMaker
*.env файл специально оставлен в гите чтобы не делать доп действия с envexampe и тд)*

### Run docker compose:
```bash
docker compose -f compose.yaml up -d
```

### Swagger:
[Тык](http://127.0.0.1:8000/api/v1/docs#)

### Endpoints:
**GET /api/v1/events/**
```
Get all events from Line Provider through Kafka
```
** GET /api/v1/bets/**
```
Get all bets
```

**POST /api/v1/bet/**
```
Get all bets
```

#### TODO: 
1. Make custom exception handlers, but later)