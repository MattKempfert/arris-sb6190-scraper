default: dev

dev:
	pip install --upgrade pip
	pip install --requirement requirements.txt

build:
	 docker build -t scrape:v1 .

run:
	docker run scrape:v1
