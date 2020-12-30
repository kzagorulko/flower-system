all: run

run:
	uvicorn start:app --reload --workers 2

test:
	psql -c "drop database if exists flower_test" postgres
	psql -c "drop user if exists flower_test_user" postgres
	psql -c "create user flower_test_user" postgres
	psql -c "create database flower_test" postgres
	TESTING=True python3 -m pytest --cov=flower

test-ci:
	sudo -u postgres psql -c "drop database if exists flower_test"
	sudo -u postgres psql -c "drop user if exists flower_test_user"
	sudo -u postgres psql -c "create user flower_test_user"
	sudo -u postgres psql -c "create database flower_test"
	TESTING=True python3 -m pytest --cov=flower

db-migrate:
	alembic revision --autogenerate

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1
