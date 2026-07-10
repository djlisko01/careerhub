BACKEND_DIR := ./backend

############################ Backend Commands #############################

test_backend:
	@echo "Running backend tests..."
	uv run --directory ${BACKEND_DIR} pytest

uv_sync:
	@echo "Synchronizing backend dependencies..."
	uv run --directory ${BACKEND_DIR} uv sync

uv_sync_dev:
	@echo "Synchronizing backend dependencies for development..."
	uv run --directory ${BACKEND_DIR} uv sync --dev

######################### API Commands ##############################
run_api_dev:
	@echo "Running FastAPI development server..."
	uv run --directory ${BACKEND_DIR}/app fastapi dev

########################### Docker  DB SERVICES #############################
docker_start_db:
	@echo "Starting database container..."
	docker-compose up -d db

docker_down_db:
	@echo "Tearing down database container..."
	docker-compose down

docker_clean_db:
	@echo "Cleaning up database container..."
	docker-compose down -v --remove-orphans
	@echo "Database container cleaned up."

db_migrate:
	@echo "Migrating database..."
	uv run --directory ${BACKEND_DIR} alembic upgrade head