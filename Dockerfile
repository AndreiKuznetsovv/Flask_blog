FROM python:3.10-slim

WORKDIR /flask_blog

COPY requirements.txt requirements.txt
RUN python -m venv venv
RUN venv/bin/pip install -r requirements.txt

COPY website website
COPY migrations migrations
COPY app.py data.json .env boot.sh ./

EXPOSE 8080
ENTRYPOINT ["./boot.sh"]
