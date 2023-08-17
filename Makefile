.PHONY: lint
lint:
	flake8 .
	mypy .

.PHONY: po
po:
	python manage.py makemessages --no-wrap --locale=en --locale=ru -i=*env

.PHONY: mo
mo:
	python manage.py compilemessages --locale=en --locale=ru -i=*env

.PHONY: mm
mm:
	python manage.py makemigrations

.PHONY: mg
mg:
	python manage.py migrate

.PHONY: csu
csu:
	python manage.py createsuperuser

.PHONY: run
run:
	python manage.py runserver
