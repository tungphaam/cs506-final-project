# Define variables
VENV = venv
PYTHON = python3
FLASK_APP = app.py
PIP = $(VENV)/bin/pip
FLASK = $(VENV)/bin/flask
PYTHON_BIN = $(VENV)/bin/python

.PHONY: install run clean reinstall test

# Create virtual environment and install dependencies
install:
	@echo "Creating virtual environment and installing dependencies..."
	$(PYTHON) -m venv $(VENV)
	$(PIP) install --upgrade pip
	$(PIP) install -r requirements.txt

# Run the Flask application
run:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Running install first..."; \
		make install; \
	fi
	@echo "Starting Flask application..."
	FLASK_APP=$(FLASK_APP) FLASK_ENV=development $(FLASK) run --port 3000

# Clean up virtual environment
clean:
	@echo "Cleaning up virtual environment and temporary files..."
	rm -rf $(VENV)
	find . -type f -name "*.pyc" -delete
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.log" -delete

# Reinstall all dependencies
reinstall: clean install

# Run tests
test:
	@if [ ! -d "$(VENV)" ]; then \
		echo "Virtual environment not found. Running install first..."; \
		make install; \
	fi
	@echo "Running unit tests with pytest..."
	PYTHONPATH=$(shell pwd) $(VENV)/bin/pytest

