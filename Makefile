.PHONY: help install run-api run-dashboard test docker-build docker-up docker-down clean init-db train-models

help:
	@echo "Available commands:"
	@echo "  make install      - Install dependencies"
	@echo "  make run-api      - Run API server"
	@echo "  make run-dashboard- Run Streamlit dashboard"
	@echo "  make test         - Run tests"
	@echo "  make docker-build - Build Docker images"
	@echo "  make docker-up    - Start all services"
	@echo "  make docker-down  - Stop all services"
	@echo "  make init-db      - Initialize database"
	@echo "  make train-models - Train ML models"
	@echo "  make clean        - Clean temporary files"

install:
	pip install -r requirements.txt

run-api:
	uvicorn api.main:app --reload --host 0.0.0.0 --port 8000

run-dashboard:
	streamlit run dashboard/app.py

test:
	pytest tests/ -v --cov=. --cov-report=html

docker-build:
	docker-compose build

docker-up:
	docker-compose up -d
	@echo "Services started:"
	@echo "  API: http://localhost:8000"
	@echo "  Dashboard: http://localhost:8501"
	@echo "  PostgreSQL: localhost:5432"
	@echo "  Redis: localhost:6379"

docker-down:
	docker-compose down

docker-logs:
	docker-compose logs -f

init-db:
	python scripts/init_db.py

train-models:
	python scripts/train_models.py

clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.db" -delete
	rm -rf .pytest_cache
	rm -rf htmlcov
	rm -rf logs/
	rm -rf models/*.pkl

dev: install init-db
	@echo "Starting development environment..."
	$(MAKE) run-api &
	$(MAKE) run-dashboard

all: docker-build docker-up
	@echo "System is ready!"