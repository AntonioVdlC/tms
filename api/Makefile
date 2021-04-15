build:
	docker-compose build

up: down build
	docker-compose up -d
	make logs

logs:
	docker-compose logs -f api

down:
	docker-compose down --remove-orphans

reload:
	docker-compose up -d --no-deps --build api
	make logs