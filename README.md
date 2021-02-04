# Flower ERP

ERP система для сети цветочных магазинов 🌸

Содержание:
- [Кратко о проекте, демо](https://github.com/kzagorulko/flower-system#%D0%BA%D1%80%D0%B0%D1%82%D0%BA%D0%BE-%D0%BE-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B5)
- [Как развернуть систему](https://github.com/kzagorulko/flower-system#%D0%BA%D0%B0%D0%BA-%D1%80%D0%B0%D0%B7%D0%B2%D0%B5%D1%80%D0%BD%D1%83%D1%82%D1%8C-%D1%81%D0%B8%D1%81%D1%82%D0%B5%D0%BC%D1%83)
- [Wiki проекта](https://github.com/kzagorulko/flower-system#wiki-%D0%BF%D1%80%D0%BE%D0%B5%D0%BA%D1%82%D0%B0)
- [Лицензия](https://github.com/kzagorulko/flower-system#%D0%BB%D0%B8%D1%86%D0%B5%D0%BD%D0%B7%D0%B8%D1%8F)

## Кратко о проекте

Система разработана в рамках дисциплины информатизации предприятия.

Предприятие для информатизации - цветочный магазин, состоящий из некоторого количества филиалов. 

_пример смены склада для закупки, просьба выражена в заявке_

![пример смены склада для закупки](https://user-images.githubusercontent.com/30318463/106644860-b28fbc80-659c-11eb-8d86-7bfcd5a21c19.gif)


Что было автоматизировано (основное):
- Работа с филиалами:
  - Хранение филиалов
  - Привязка пользователей в филиалам
  - Отчеты о продажах и закупках
- Работа с товарами
- Работа со поставщиками и складами (отчеты о доставке товара на склад, о доставке товара в филиал, ...)
- Система заявок
- Система доступа (три отдела: отдел логистики, юр.отдел и отдел продаж)

### Онлайн

[http://flower-system.herokuapp.com/](http://flower-system.herokuapp.com/)

- login: demo
- password: demo


## Как развернуть систему

### Нативно

Необходимо выполнить следующие шаги:
1. Развернуть `frontend` по [инструкции](https://github.com/kzagorulko/flower-system/tree/develop/frontend#setup-and-run)

Для локальной разработки используется сервер `node` (по ссылке `run at localhost:3000`)

2. Установить [PostgreSQL](https://www.postgresql.org/download/)

3. Развернуть `backend` по [инструкции](https://github.com/kzagorulko/flower-system/tree/develop/backend#initial-setup)

После выполнения `frontend` часть будет доступна по адресу `localhost:3000`; `backend` будет запущен на `localhost:8000`

### Через Docker

Есть возможность использовать `docker`, однако базу данных [PostgreSQL](https://www.postgresql.org/download/) необходимо развернуть отдельно, указав в 
файле `/beckend/.env.local` нужные данные подключения (в примере - дефолтные значения):

```env
DB_HOST=localhost
DB_PORT=5432
DB_USER=flower_dev_user
DB_PASSWORD=flower_dev_user
DB_DATABASE=flower_dev
```

Также необходимо в окружение поместить переменную `PORT`; она используется для запуска `nginx` внутри контейнера

```bash
> export PORT=80
```

`Dockerfile` находится в корне проекта:

```bash
# run at localhost:80
> docker build --build-arg FRONT_API_URL=/api -t flower-system .
> docker run -p 80:80 --env PORT=80 --name flower-system flower-system
```

## Wiki проекта

К Wiki можно получить доступ по [ссылке](https://github.com/kzagorulko/flower-system/wiki)

Состав Wiki:
- [Описание](https://github.com/kzagorulko/flower-system/wiki/%D0%9E%D0%BF%D0%B8%D1%81%D0%B0%D0%BD%D0%B8%D0%B5-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87%D0%B8) - краткое изложение поставленной задачи, аналоги
- [Примеры](https://github.com/kzagorulko/flower-system/wiki/%D0%9F%D1%80%D0%B8%D0%BC%D0%B5%D1%80%D1%8B) - некоторые из случаей из работы предприятия, которые нужно было автоматизировать
- [ERD-Диаграмма](https://github.com/kzagorulko/flower-system/wiki/ERD-%D0%B4%D0%B8%D0%B0%D0%B3%D1%80%D0%B0%D0%BC%D0%BC%D0%B0) базы данных
- [Ролевая модель](https://github.com/kzagorulko/flower-system/wiki/%D0%A0%D0%BE%D0%BB%D0%B5%D0%B2%D0%B0%D1%8F-%D0%BC%D0%BE%D0%B4%D0%B5%D0%BB%D1%8C) - диаграмма ролей и доступов
- [Предварительная декомпозиция задач](https://github.com/kzagorulko/flower-system/wiki/%D0%9F%D1%80%D0%B5%D0%B4%D0%B2%D0%B0%D1%80%D0%B8%D1%82%D0%B5%D0%BB%D1%8C%D0%BD%D0%B0%D1%8F-%D0%B4%D0%B5%D0%BA%D0%BE%D0%BC%D0%BF%D0%BE%D0%B7%D0%B8%D1%86%D0%B8%D1%8F-%D0%B7%D0%B0%D0%B4%D0%B0%D1%87) - работа проводилась в команде; страница создавалась в начале ведения проекта; итоговые задачи доступны во вкладке [Projects](https://github.com/kzagorulko/flower-system/projects/1)
- [Backend API](https://github.com/kzagorulko/flower-system/wiki/Backend-API) - документация `API`
- [Frontend Framework](https://github.com/kzagorulko/flower-system/wiki/Frontend-framework) - описание материалов для разработки `frontend` части проекта

Кроме `Wiki`, существует менее структурированная документация о проекте; например, в `/backend/flower/core` можно найти [методику написания роутов](https://github.com/kzagorulko/flower-system/tree/develop/backend/flower/core) для `backend` части - кейсы реализации роутов являлись типовыми задачами в разработке серверной части

## Лицензия

Лицензия [MIT](https://github.com/kzagorulko/flower-system/blob/develop/LICENSE)
