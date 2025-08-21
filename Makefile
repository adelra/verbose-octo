.PHONY: build test cleanup lint check

build:
	docker-compose build

test:
	docker-compose run --rm tester

cleanup:
	docker-compose down --remove-orphans
	docker image prune -f

lint:
	docker-compose run --rm tester ruff format src tests

check:
	docker-compose run --rm tester ruff check src tests
