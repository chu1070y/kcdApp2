# 실행방법

> config/config.ini에 ip주소 변경 필요

##### 도커 빌드

```
docker build -t kcdapp2 .
```

##### docker compose (App & PostgreSQL)

```
docker-compose -f ./docker-compose.yml up -d
```

##### App only

```
docker run -it -d --network kcd_network --name kcdapp2 kcdapp2
```

##### pg 접속

```
docker exec -it postgres /bin/bash
psql -U gwchu -d kcd
```
