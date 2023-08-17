## Запуск проекта в режиме разработчика

### Клонировать репозиторий
```
git clone https://github.com/GritsenkoSerge/django_sample
```
### Перейти в директорию проекта
```
cd django_sample
```
### Создать/обновить виртуальное окружение с помощью poetry
```
poetry update
```
### Активировать виртуальное окружение
```
poetry shell
```
### Скопировать файл `.env.example` в `.env` и задать значения переменным
```
cp .env.example .env
```

| Переменная | Значение по умолчанию | Описание |
| --- | --- | --- |
| DEBUG | False | Режим отладки |
| SECRET_KEY | None | `from django.core.management.utils import get_random_secret_key; get_random_secret_key()` |
| ALLOWED_HOSTS | * | Список разрешенных хостов, указанных через пробел |
| POSTGRES_DB | postgres_db | Имя базы данных |
| POSTGRES_USER | postgres_user | Имя пользователя (владельца) базы данных |
| POSTGRES_PASSWORD | postgres_pass | Пароль пользователя (владельца) базы данных |
| POSTGRES_HOST | 127.0.0.1 | ip-адрес хоста, на котором находится база данных |
| POSTGRES_PORT | 5432 | порт, который слушает база данных |

### Перейти в директорию infra/dev/
```
cd infra/dev/
```
### Скопировать файл с переменными окружения
```
cp ../../.env .
```
### Запустить контейнер с базой данных PostgreSQL
```
docker compose up -d
```
### Вернуться в директорию проекта
```
cd ../..
```
### Применить миграции
```
make mg
```
### Сгенерировать файл с переводами на русский язык
```
make mo
```
### Создать суперпользователя
```
make csu
```
### Запустить сервер
```
make run
```
### Ссылки
- Открыть страницы документации API:
  * [api.yaml](http://localhost:8000/api/schema/)
  * [swagger-ui](http://localhost:8000/api/schema/swagger-ui/)
  * [redoc](http://localhost:8000/api/schema/redoc/)
- Открыть панель администратора [http://localhost:8000/admin/](http://localhost:8000/admin/)
