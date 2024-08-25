FROM python:3.12-slim

RUN apt-get update && \
    apt-get install -y libreoffice unoconv

WORKDIR /app

COPY . ./

ENV PORT 8000
RUN pip3 install --no-cache-dir -r requirements.txt

CMD exec uvicorn api:app --host 0.0.0.0 --port 8000