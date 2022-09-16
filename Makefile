SHELL := /bin/bash

default: install test

install:
	# Upgrade pip
	pip install --upgrade pip

	# Install script dependencies
	pip install --requirement requirements.txt

test:
	# Install testing dependencies
	pip install --requirement requirements-test.txt
	flake8 --statistics --count

run: install test
	# Execute script locally
	python scraper/main.py status

run-on-pi:
	# Activate a virtual env and run script
	source env/bin/activate && \
	source .env && \
	python scraper/main.py status && \
	deactivate
