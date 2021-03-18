.PHONY: logs services up-app build-app exec-app stop-app down

logs:
	docker-compose logs -f

services:
	docker-compose up -d mysql redis grafana

up-app:
	docker-compose up -d app

build-app:
	docker-compose up --build -d app

exec-app:
	docker-compose exec app bash

stop-app:
	docker-compose stop app
	docker-compose rm app

down:
	docker-compose down -v