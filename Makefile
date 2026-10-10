.PHONY: up down test attack logs backup

ifeq ($(OS),Windows_NT)
PYTHON := py -3.12
else
PYTHON := python3
endif

up:
	docker compose up -d --build

down:
	docker compose down --remove-orphans

test:
	$(PYTHON) -m pytest -q ehr_app/test_app.py tests/test_policy.py

attack:
	docker compose exec attacker /attack/attack.sh

logs:
	docker compose logs -f --tail=100

backup:
	sh scripts/backup.sh
