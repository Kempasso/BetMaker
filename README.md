# BetMaker

*!NOTE!: This service must be started first!*

*Next, start the microservice https://github.com/Kempasso/LineProvider*

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
Make bet
```

#### TODO: 
1. Make custom exception handlers, but later)