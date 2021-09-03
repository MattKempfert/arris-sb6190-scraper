default: install test

install:
	# Upgrade pip
	pip3 install --upgrade pip

	# Install script dependencies
	pip3 install --requirement requirements.txt

test:
	# Install testing dependencies
	pip3 install --requirement requirements-test.txt
	flake8 --statistics --count

run-local: install test
	# Execute script locally
	python3 scrape.py

build:
	# Build Docker image
	 docker build -t scrape:v1 .

run:
	# Execute script through a Docker container
	docker run scrape:v1
