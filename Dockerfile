# Diving into docker

FROM python:3.10-alpine

LABEL version="1.0"

RUN mkdir /app

WORKDIR /app

COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY main.py /app/main.py

COPY ./src /app/src

EXPOSE 8050/tcp

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8050"]