.PHONY: up down test attack logs

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

test:
	docker compose run --rm test

attack:
	docker compose run --rm attacker

logs:
	docker compose logs -f --tail=100

