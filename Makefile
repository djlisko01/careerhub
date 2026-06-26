BACKEND_DIR := ./backend

test_backend:
	@echo "Running backend tests..."
	uv run --directory ${BACKEND_DIR} pytest

uv_sync:
	@echo "Synchronizing backend dependencies..."
	uv run --directory ${BACKEND_DIR} uv sync

uv_sync_dev:
	@echo "Synchronizing backend dependencies for development..."
	uv run --directory ${BACKEND_DIR} uv sync --dev

docker_start_db:
	@echo "Starting database container..."
	docker-compose up -d db

docker_stop_db:
	@echo "Stopping database container..."
	docker-compose down

docker_clean_db:
	@echo "Cleaning up database container..."
	docker-compose down -v --remove-orphans
	