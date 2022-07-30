FROM python:3.9.13-buster

WORKDIR /code

COPY  requirements.txt . 

RUN pip install --no-cache-dir --upgrade -r requirements.txt


COPY . . 

EXPOSE 80

CMD ["uvicorn", "main:app", "--proxy-headers", "--host", "0.0.0.0", "--port", "80"]
