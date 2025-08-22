.PHONY: build test cleanup lint check help run

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

notebook:
	docker-compose build
	docker-compose run --rm -p 8888:8888 -v ~/.cache/huggingface/datasets:/root/.cache/huggingface/datasets api jupyter lab --ip=0.0.0.0 --port=8888 --allow-root --no-browser --NotebookApp.token='coco'

run:
	docker-compose up api

help:
	@echo "Available commands:"
	@echo "  build     - Build Docker images"
	@echo "  test      - Run tests"
	@echo "  cleanup   - Clean up Docker resources"
	@echo "  lint      - Run linter (ruff format)"
	@echo "  check     - Run linter (ruff check)"
	@echo "  notebook  - Start Jupyter Lab notebook"
	@echo "  run       - Start the FastAPI server using Docker Compose"
	@echo "  help      - Display this help message"
