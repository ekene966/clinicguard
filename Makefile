.PHONY: up down test attack logs

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

test:
	py -3.12 -m pytest -q tests/test_policy.py

attack:
	docker compose exec attacker /attack/attack.sh

logs:
	docker compose logs -f --tail=100
