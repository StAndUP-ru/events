# ya-events-backend

## Стек технологий
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)](https://www.python.org/)
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)](https://www.djangoproject.com/)
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)](https://www.django-rest-framework.org/)
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)](https://www.postgresql.org/)
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)](https://nginx.org/ru/)
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)](https://gunicorn.org/)
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)](https://www.docker.com/)

## Развертывание в режиме разработчика
### Клонировать репозиторий
```
git clone git@github.com:StAndUP-ru/events.git
```
### Перейти в директорию events
```
cd events
```
### Создать виртуальное окружение
```
python3.11 -m venv venv
```
### Активировать виртуальное окружение
```
. ./venv/bin/activate
```
### Обновить установщик пакетов pip
```
pip install --upgrade pip
```
### Установить зависимости
```
pip install -r requirements.txt
```
### В директории events_app скопировать файл `.env.example` в `.env` и задать значения переменным
