all: run

run:
	uvicorn start:app --reload --workers 2

db-migrate:
	alembic revision --autogenerate

db-upgrade:
	alembic upgrade head

db-downgrade:
	alembic downgrade -1
