FROM python:3.8-slim-buster

WORKDIR /app

EXPOSE 8001

ENV FLASK_ENV=development

COPY . /app
RUN pip install -r requirements.txt

CMD [ "python3",  "app.py"]