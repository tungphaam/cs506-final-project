.PHONY: all clean install test run

# Default target
all: install test run

# Install dependencies
install:
	python -m pip install --upgrade pip
	pip install -r requirements.txt

# Run tests
test:
	python -m pytest tests/

# Run the model
run:
	python boston_budget.py

# Clean up generated files
clean:
	find . -type d -name "__pycache__" -exec rm -rf {} +
	find . -type f -name "*.pyc" -delete
	find . -type f -name "*.pyo" -delete
	find . -type f -name "*.pyd" -delete
	find . -type d -name "*.egg-info" -exec rm -rf {} +
	find . -type f -name ".coverage" -delete
	find . -type d -name ".pytest_cache" -exec rm -rf {} +
