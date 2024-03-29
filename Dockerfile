FROM python:3.10.8-buster

WORKDIR /code

COPY  ./requirements.txt /code/requirements.txt


RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
COPY ./app /code/app


EXPOSE 7001

CMD ["uvicorn", "app.main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "7001"]
