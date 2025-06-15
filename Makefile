#################################################################################
# GLOBALS                                                                       #
#################################################################################

PROJECT_NAME = data_movies
PYTHON_VERSION = 3.10
PYTHON_INTERPRETER = python

#################################################################################
# COMMANDS                                                                      #
#################################################################################

## Install Python dependencies via Poetry
.PHONY: install
install:
	poetry install

## Install Python dependencies
.PHONY: requirements
requirements:
	pip install -e .
	



## Delete all compiled Python files
.PHONY: clean
clean:
	find . -type f -name "*.py[co]" -delete
	find . -type d -name "__pycache__" -delete


## Lint using flake8, black, and isort (use `make format` to do formatting)
.PHONY: lint
lint:
	flake8 ./scripts 
	isort --check --diff ./scripts ./tests 
	black --check ./scripts 

## Format source code with black
.PHONY: format
format: 
	black scripts tests 
	isort scripts tests

## Run tests with pytest (use `make test`)
.PHONY: test
test:
	pytest tests


