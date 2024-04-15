FROM python:3.11-slim

ENV APP_HOME=/event_app

RUN apt-get update \
    && apt-get upgrade -y \
    && apt-get install gettext libpq-dev gcc -y

RUN pip install --upgrade pip

WORKDIR $APP_HOME
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV DJANGO_SETTINGS_MODULE event_app.settings

RUN addgroup --system backend_user \
    && adduser --system --ingroup backend_user backend_user

COPY entrypoint.sh entrypoint.sh
COPY ./event_app .

RUN  mkdir static media \
    && chown -R backend_user:backend_user $APP_HOME

RUN  sed -i 's/\r$//' ./entrypoint.sh && chmod +x ./entrypoint.sh

USER backend_user

ENTRYPOINT  ["./entrypoint.sh"]
