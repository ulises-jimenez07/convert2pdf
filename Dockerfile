FROM python:3.9

WORKDIR /code

COPY ./requirements.txt /code/requirements.txt

RUN pip install --no-cache-dir --upgrade -r /code/requirements.txt
 
COPY ./app /code/app

ENV PORT=8080

EXPOSE 8080

CMD ["fastapi", "run", "app/main.py", "--port", "8800"]