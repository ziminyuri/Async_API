FROM python:3.10-slim-buster

WORKDIR /usr/src/app

#EXPOSE 80

COPY ./requirements.txt requirements.txt

RUN pip install --no-cache-dir --upgrade -r requirements.txt

COPY ./src .

CMD ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]
