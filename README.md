# Веб-приложение для Funtech
![GitHub repo size](https://img.shields.io/github/repo-size/StAndUP-ru/events?) 
![Static Badge](https://img.shields.io/badge/test_coverage-92%25-F) 
![GitHub language count](https://img.shields.io/github/languages/count/StAndUP-ru/events)
![GitHub commit activity](https://img.shields.io/github/commit-activity/w/StAndUP-ru/events)
  
Единая платформа для IT-специалистов, где они смогут легко находить и регистрироваться на мероприятия, обмениваться знаниями и устанавливать профессиональные связи
## I. Сведения о команде

| роль в проекте | имя и фамилия | контакты 
| ------ | ------ |  ------ |
| Project Manager |  Мария Уракова  | https://t.me/uramasha
| Product Manager | Александр Леванов  | https://t.me/Aleksandr_Levanov
| UX/UI Designer | Елена Отт | https://t.me/lena_ott
| UX/UI Designer | Анна Ненашева | https://t.me/AnnaNenashevaNL
| Systems Analyst | Екатерина Васильева | https://t.me/tiramisuspb
| Systems Analyst | Наталья Баптиданова  | https://t.me/texdecor
| Systems Analyst | Василиса Беспалая  | https://t.me/Lisadereza
| Business Analyst | Елена Сафонова  | https://t.me/ElenaS_SEA
| Frontend Developer | Владислав Сердюков | https://t.me/VladisSerd
| Backend Developer | Сергей Барышевский  | https://t.me/Rexten
| Backend Developer | Станислав Андрющенко | https://t.me/StAndSt
| Backend Developer | Дмитрий Печенков | https://t.me/imperatorObi1Kenobi


## II. Документация API
http://funtech.b2k.me/api/v1/swagger/
http://funtech.b2k.me/api/v1/redoc/
## III. Инструкция по сборке и запуску
### Backend
I. Клонирование репозитория проекта с субмодулями
```sh
git clone --recurse-submodules git@github.com:StAndUP-ru/funtech.git
```
II.a) Подготовка Backend для **Linux/MacOS**
```
cd events
python3.11 -v venv venv
source venv/bin/activate
pip install --upgrade pip
pip install -r requirements.txt
```
II.b) Подготовка Backend для **Windows**
```sh
cd events
python -3.11 -m venv venv
venv\Scripts\activate.ps1
python -m install pip --upgrade pip
pip install -r requirements.txt
```
III. В директории events_app скопировать файл `.env.example` в `.env` и задать значения переменным
IV Тестирование
```sh
cd events
pytest event_app
```
### Frontend
```sh
cd funtech-front
npn install
npn run dev
```
### Продакшн запуск (Docker-compose)
```sh
cd infra/dev
docker compose pull
docker compose up
```
Рекомендуется настройка Workflow на базе [GitHub Actions]. Все необходимые workflow файлы в репозитории. Необходимо добавить GitHub variables & secrets перед запуском.
## IV. Cтэк технологий 
[![Python](https://img.shields.io/badge/-Python-464646?style=flat-square&logo=Python)]([Python])
[![Python](https://img.shields.io/badge/-TypeScript-464646?style=flat-square&logo=TypeScript)]([Typescript])
[![Python](https://img.shields.io/badge/-React-464646?style=flat-square&logo=React)]([React])
[![Django](https://img.shields.io/badge/-Vite-464646?style=flat-square&logo=Vite)]([Vite])
[![Django](https://img.shields.io/badge/-Zod-464646?style=flat-square&logo=Zod)]([Zod])
[![Django](https://img.shields.io/badge/-Remix-464646?style=flat-square&logo=Remix)]([Remix])
[![Django](https://img.shields.io/badge/-SASS-464646?style=flat-square&logo=SASS)]([SASS])
[![Django](https://img.shields.io/badge/-MobX-464646?style=flat-square&logo=Mobx)]([Mobx])
[![Django](https://img.shields.io/badge/-React_hook_form-464646?style=flat-square&logo=react%20hook%20form)]([ReactHookForm])
[![Django](https://img.shields.io/badge/-Django-464646?style=flat-square&logo=Django)]([Django])
[![Django REST Framework](https://img.shields.io/badge/-Django%20REST%20Framework-464646?style=flat-square&logo=Django%20REST%20Framework)]([Django_Rest_Framework_(DRF)])
[![PostgreSQL](https://img.shields.io/badge/-PostgreSQL-464646?style=flat-square&logo=PostgreSQL)]([PostgreSQL])
[![Nginx](https://img.shields.io/badge/-NGINX-464646?style=flat-square&logo=NGINX)]([Nginx])
[![gunicorn](https://img.shields.io/badge/-gunicorn-464646?style=flat-square&logo=gunicorn)]([Gunicorn])
[![Django](https://img.shields.io/badge/-Celery-464646?style=flat-square&logo=Celery)]([Celery])
[![Django](https://img.shields.io/badge/-Redis-464646?style=flat-square&logo=Redis)]([Redis])
[![Django](https://img.shields.io/badge/-Pytest-464646?style=flat-square&logo=Pytest)]([Pytest])
[![docker](https://img.shields.io/badge/-Docker-464646?style=flat-square&logo=docker)]([Docker])


- [TypeScript] - TypeScript
- [Python] - Python 3.11
- [React] - Frontend framework
- [Django] - Backend Web framework
- [Django_Rest_Framework_(DRF)] - REST API Framework для Django
- [PostgreSQL] - Open Source Database & DMBS
- [Docker] - Docker и docker hub для сборки и управления образами
- [Nginx] - Web-сервер и обратный прокси
- [GitHub Actions] - Сервис для имплементации CI/CD

## V. Cсылки на сторонние фреймворки, библиотеки, иконки и шрифты если использовались
- [Vite] - Инструмент сборки
- [Zod] - Валидатор схемы данных с поддержкой TypeScript
- [Remix] - Remix framework для SSR
- [SASS] - Extended CSS Preprocessor
- [Mobx] - State management
- [ReactHookForm] - Инструмент создания и валидации форм для React
- [Gunicorn] - WSGI Server для Django
- [Celery] = Менеджер очередей
- [Redis] - Брокер сообщений и хранилище данных
- [Pytest] - Python testing framework

## License

This project is licensed under the MIT License - see the [LICENSE] file for details

![Иллюстрация к проекту](http://funtech.b2k.me/assets/Illustration_Community-DXMb6J5j.png)

[//]: # (These are reference links used in the body of this note and get stripped out when the markdown processor does its job. There is no need to format nicely because it shouldn't be seen. Thanks SO - http://stackoverflow.com/questions/4823468/store-comments-in-markdown-syntax)

   [git-repo-url]: <https://github.com/StAndUP-ru/funtech.git>
   [Django]: <https://www.djangoproject.com>
   [Python]: <https://www.python.org/>
   [Typescript]: <https://www.typescriptlang.org/>
   [Django_Rest_Framework_(DRF)]: <https://www.django-rest-framework.org/>
   [PostgreSQL]: <https://www.postgresql.org/>
   [Nginx]: <https://nginx.org/ru/>
   [Gunicorn]: <https://gunicorn.org/>
   [Celery]: <https://docs.celeryq.dev/en/stable/>
   [Redis]: <https://redis.io/>
   [Pytest]: <https://pytest.org>
   [Dillinger.io]: <https://dillinger.io/>
   [React]: <https://react.dev/>
   [Vite]: <https://vitejs.dev/>
   [Zod]: <https://zod.dev/>
   [Remix]: <https://remix.run/>
   [SASS]: <https://sass-lang.com/>
   [Mobx]: <https://mobx.js.org/>
   [ReactHookForm]: <https://react-hook-form.com/>
   [Docker]: <https://www.docker.com/>
   [GitHub Actions]: <https://github.com/features/actions>
   [LICENSE]: <https://github.com/StAndUP-ru/funtech/blob/develop/LICENSE>
