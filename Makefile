.PHONY: install clean lint test coverage build docs help

# Python interpreter to use
PYTHON := python3
PIP := pip3

# Project directories
SRC_DIR := jutix
TEST_DIR := tests
DOCS_DIR := docs
BUILD_DIR := build
DIST_DIR := dist

# Virtual environment
VENV := venv
VENV_BIN := $(VENV)/bin

help:
	@echo "Available commands:"
	@echo "  make install      - Install the package"
	@echo "  make clean        - Clean build directories and cache files"
	@echo "  make lint         - Run code linting (flake8, mypy)"
	@echo "  make test         - Run tests"
	@echo "  make coverage     - Run tests with coverage report"
	@echo "  make build        - Build package distribution"
	@echo "  make docs         - Generate documentation"

install:
	$(PIP) install .

clean:
	rm -rf $(BUILD_DIR) $(DIST_DIR) .coverage .pytest_cache .mypy_cache
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete

lint:
	flake8 $(SRC_DIR)
	mypy $(SRC_DIR)
	black --check $(SRC_DIR)
	isort --check-only $(SRC_DIR)

format:
	black $(SRC_DIR)
	isort $(SRC_DIR)

test:
	pytest $(TEST_DIR)

coverage:
	pytest --cov=$(SRC_DIR) $(TEST_DIR) --cov-report=html --cov-report=term

build:
	$(PYTHON) -m build

docs:
	cd $(DOCS_DIR) && make html

# Development environment setup
setup-dev: clean
	$(PYTHON) -m venv $(VENV)
	$(VENV_BIN)/pip install --upgrade pip
	$(VENV_BIN)/pip install -e ".[dev]"
	$(VENV_BIN)/pip install -r requirements-dev.txt

# Run the application
run:
	$(PYTHON) -m jutix.main $(ARGS)

# Default target
.DEFAULT_GOAL := help

