FROM python:3.10-slim

RUN apt-get update

WORKDIR /app 
COPY . .

RUN pip install --upgrade pip 
RUN pip install -r requirements.txt 

EXPOSE 8080

CMD [ "python",  "main.py"]