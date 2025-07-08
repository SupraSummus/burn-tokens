.PHONY: help install test lint format run clean docker-build docker-run

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies
	pip install -r requirements.txt

test: ## Run tests
	pytest tests/ -v

lint: ## Run linting
	flake8 app.py tests/ conftest.py

format: ## Format code
	black app.py tests/ conftest.py

run: ## Run the application
	python app.py

clean: ## Clean cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

docker-build: ## Build Docker image
	docker build -t burn-tokens .

docker-run: ## Run Docker container
	docker run --rm -p 5000:5000 burn-tokens

docker-compose-up: ## Start with docker-compose
	docker-compose up --build

docker-compose-down: ## Stop docker-compose
	docker-compose down

dev-setup: install ## Set up development environment
	cp .env.example .env
	@echo "Development environment set up!"
	@echo "Edit .env file with your configuration"

ci: lint test ## Run CI checks locally
	@echo "All CI checks passed!"