default: dev

dev:
	pip install --upgrade pip
	pip install --requirement requirements.txt

run:
	python scrape.py
