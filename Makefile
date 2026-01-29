.PHONY: install run test verify clean reset-db help bootstrap

PORT ?= 8000

help:
	@echo "Available targets:"
	@echo "  make bootstrap - First-time setup (installs uv, dependencies)"
	@echo "  make install   - Install dependencies"
	@echo "  make run       - Start dev server (PORT=8000 by default)"
	@echo "  make run PORT=3000 - Start on custom port"
	@echo "  make test      - Run test suite"
	@echo "  make verify    - Verify setup"
	@echo "  make reset-db  - Reset database with fresh seed data"
	@echo "  make clean     - Remove generated files"

bootstrap:
	@./scripts/bootstrap.sh

install:
	uv sync --all-extras

run:
	uv run python -c "import uvicorn; uvicorn.run('src.main:app', host='0.0.0.0', port=$(PORT), reload=True)"

test:
	uv run pytest --tb=short -q

test-verbose:
	uv run pytest -v

verify:
	@./scripts/verify-setup.sh

reset-db:
	rm -f data.db
	uv run python -c "from src.database import init_db, seed_db; init_db(); seed_db()"
	@echo "Database reset complete"

clean:
	rm -f data.db
	rm -rf __pycache__ src/__pycache__ tests/__pycache__
	rm -rf .pytest_cache
	find . -name "*.pyc" -delete
