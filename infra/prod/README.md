## Запуск проекта

### Клонировать репозиторий
```
git clone https://github.com/GritsenkoSerge/hammer_systems_task
```
### Перейти в директорию hammer_systems_task/infra/prod
```
cd hammer_systems_task/infra/prod
```
### Скопировать файл `.env.example` в `.env`, при необходимости задать значения переменным
```
cp .env.example .env
```

| Переменная | Значение по умолчанию | Описание |
| --- | --- | --- |
| DEBUG | False | Режим отладки |
| SECRET_KEY | None | `from django.core.management.utils import get_random_secret_key; get_random_secret_key()` |
| ALLOWED_HOSTS | * | Список разрешенных хостов, указанных через пробел |
| CSRF_TRUSTED_ORIGINS | | Список доверенных источников для небезопасных запросов |
| POSTGRES_DB | postgres_db | Имя базы данных |
| POSTGRES_USER | postgres_user | Имя пользователя (владельца) базы данных |
| POSTGRES_PASSWORD | postgres_pass | Пароль пользователя (владельца) базы данных |
| POSTGRES_HOST | postgres | ip-адрес хоста, на котором находится база данных |
| POSTGRES_PORT | 5432 | порт, который слушает база данных |

### Запустить контейнер с базой данных PostgreSQL
```
docker compose up -d --build
```
### Ссылки
- Открыть страницы документации API:
  * [api.yaml](http://localhost:8080/api/schema/)
  * [swagger-ui](http://localhost:8080/api/schema/swagger-ui/)
  * [redoc](http://localhost:8080/api/schema/redoc/)
- Открыть панель администратора [http://localhost:8080/admin/](http://localhost:8080/admin/)
### Создать суперпользователя
- подключиться к контейнеру backend
```
docker compose exec backend bash
```
- запустить команду создания суперпользователя
```
python manage.py createsuperuser
```
