# Define variables
POETRY := $(shell which poetry)
#POETRY := $(shell command -v poetry 2> /dev/null)
INSTALL_STAMP := .install.stamp

# Set the default goal
.DEFAULT_GOAL := help

# Declare phony targets
.PHONY: help install clean lint format test cleaner run dev loadModels

# Help target to display available commands
help:
	@echo "Please use 'make <target>' where <target> is one of:"
	@echo ""
	@echo " install   - Install packages and prepare environment"
	@echo " loadModels- load spacy models"
	@echo " clean     - Remove all temporary files"
	@echo " cleaner   - Remove all temporary files and the .venv folder"
	@echo " lint      - Run the code linters"
	@echo " format    - Reformat code"
	@echo " test      - Run all the tests"
	@echo " dev       - Run in dev mode with auto reload"
	@echo " run       - Run in prod mode with 4 workers"
	@echo ""

# Install target to set up the environment with Poetry
install: $(INSTALL_STAMP)

$(INSTALL_STAMP): pyproject.toml
	@if [ -z $(POETRY) ]; then echo "Poetry could not be found. Please install it."; exit 2; fi
	$(POETRY) install $(POETRY_FLAGS)
	touch $(INSTALL_STAMP)

# Clean target to remove temporary files and caches
clean:
	find . -type d -name "__pycache__" | xargs rm -rf {}
	rm -rf $(INSTALL_STAMP) .coverage .mypy_cache

# Clean target to remove temporary files and caches
cleaner:
	$(MAKE) clean
	rm -rf .venv
	rm poetry.lock

# Lint target to run code linters
lint: $(INSTALL_STAMP)
	$(POETRY) run ruff check .
	$(POETRY) run mypy .

# Format target to reformat code using Black
format: $(INSTALL_STAMP)
	$(POETRY) run ruff format .

# Test target to run tests with coverage
test: $(INSTALL_STAMP)
	$(POETRY) run pytest .

# Run target to execute the application for production
dev: $(INSTALL_STAMP)
	$(POETRY) run uvicorn src.app:app --host 0.0.0.0 --port 8000 --reload

# Run target to execute the application for production
run: $(INSTALL_STAMP)
	@echo "default mode"
	$(POETRY) run uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 4

runos: $(INSTALL_STAMP)
	@echo "openshift mode"
	/home/anon/.local/bin/poetry run uvicorn src.app:app --host 0.0.0.0 --port 8000 --workers 4

loadModels: $(INSTALL_STAMP)
	$(POETRY) run python src/utils/ano_spacy.py loadModels
	