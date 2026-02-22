.PHONY: migrate upgrade downgrade test type-check lint format check infra monitoring dev debug prod down down-infra down-prod load-data

APP = web
SRC = src
POETRY = poetry run
TESTS = tests

migrate:
	docker-compose run --rm $(APP) poetry run alembic revision --autogenerate -m "$(msg)"

upgrade:
	docker-compose run --rm $(APP) alembic upgrade head

downgrade:
	docker-compose run --rm $(APP) poetry run alembic downgrade $(rev)

test:
	$(POETRY) pytest $(TESTS)

type-check:
	$(POETRY) mypy $(SRC) --explicit-package-bases

lint:
	$(POETRY) ruff check $(SRC) $(TESTS)

format:
	$(POETRY) black $(SRC) $(TESTS)
	$(POETRY) isort $(SRC) $(TESTS)

check: lint type-check test

infra:
	docker-compose -f docker-compose.infra.yml up -d --build

monitoring:
	docker compose -f docker-compose.monitoring.yml up -d

dev-web:
	docker-compose -f docker-compose.yml up --build web

dev-worker:
	docker-compose -f docker-compose.yml up --build worker

debug-web:
	docker-compose -f docker-compose.yml up --build web-debug

prod:
	docker-compose -f docker-compose.prod.yml up --build -d

down:
	docker-compose -f docker-compose.yml down

down-monitoring:
	docker-compose -f docker-compose.monitoring.yml down 

down-infra:
	docker-compose -f docker-compose.infra.yml down

down-prod:
	docker-compose -f docker-compose.prod.yml down

load-data:
	docker-compose exec $(APP) poetry run python -m scripts.load_test_data
