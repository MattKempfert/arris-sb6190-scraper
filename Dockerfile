FROM python:3.8

RUN pip install --upgrade pip

WORKDIR /app
COPY requirements.txt /app/
COPY scrape.py /app/

RUN pip install --requirement /app/requirements.txt

ENTRYPOINT ["python", "/app/scrape.py"]
