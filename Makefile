.PHONY: help install test lint format run clean

# Check if poetry is in PATH, otherwise use the local installation
POETRY := $(shell command -v poetry 2> /dev/null || echo "/home/runner/.local/bin/poetry")

help: ## Show this help message
	@echo 'Usage: make [target]'
	@echo ''
	@echo 'Targets:'
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  %-15s %s\n", $$1, $$2}' $(MAKEFILE_LIST)

install: ## Install dependencies using Poetry
	$(POETRY) install

test: ## Run tests
	$(POETRY) run pytest tests/ -v

lint: ## Run linting
	$(POETRY) run flake8 app.py tests/ conftest.py

format: ## Format code
	$(POETRY) run black app.py tests/ conftest.py

run: ## Run the application
	$(POETRY) run python app.py

clean: ## Clean cache files
	find . -type d -name __pycache__ -exec rm -rf {} + 2>/dev/null || true
	find . -type f -name "*.pyc" -delete
	rm -rf .pytest_cache

dev-setup: install ## Set up development environment
	cp .env.example .env
	@echo "Development environment set up!"
	@echo "Edit .env file with your configuration"

ci: lint test ## Run CI checks locally
	@echo "All CI checks passed!"

# Legacy commands for backwards compatibility
install-pip: ## Install dependencies using pip (legacy)
	pip install -r requirements.txt

# Poetry-specific commands
poetry-shell: ## Activate Poetry shell
	$(POETRY) shell

poetry-show: ## Show installed packages
	$(POETRY) show

poetry-update: ## Update dependencies
	$(POETRY) update