# Backend

## Initial setup


#### Virtual environment setup
```bash
python3 -m venv .venv
```

#### Database setup
(on postgres console)
```bash
create database "flower_dev";
create user "flower_dev_user" with encrypted password 'flower_dev_user';
grant all privileges on database "flower_dev" to "flower_dev_user";
```

## Day-to-day setup

```bash
source .venv/bin/activate  # enter environment
```

```bash
deactivate # exit environment
```

## Requirements

```bash
pip install -r requirements.txt # after you entered environment
```

## Running

```bash
make run
```

## Migrations

```bash
# make automatic migration
make db-migrate

# upgrade database to head
make db-upgrade

# downgrade database at one revision
make db-downgrade
```

## Tests
```bash
pytest --cov-report term --cov=flower tests/ 
```
