FROM python:3.10-slim-buster

WORKDIR /usr/src/app

EXPOSE 80

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "80"]
