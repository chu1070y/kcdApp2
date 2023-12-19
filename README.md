# 실행방법

##### 도커 빌드

```docker build -t kcdapp2 .```

##### 컨테이너 띄우기 (App & PostgreSQL)

```docker-compose -f ./docker-compose.yml up -d```

##### pg 접속

```
docker exec -it postgres /bin/bash
psql -U gwchu -d kcd
```
