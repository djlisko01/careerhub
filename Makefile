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
	