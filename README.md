# Radmin
Manager for database tokens

## Create database
- PostgreSql
```
pgcli -U postgres -d postgres -h localhost -W
```
```
CREATE ROLE radmin WITH LOGIN NOSUPERUSER CREATEDB NOCREATEROLE INHERIT NOREPLICATION CONNECTION LIMIT -1 PASSWORD 'r'
```
```
pgcli -U radmin -d postgres -h localhost -W
```
```
create database radmin
```
## Create .env in root
```
POSTGRES_URL=postgresql+asyncpg://radmin:r@localhost:5432/radmin
PRIVATE_KEY=$0123456789qwertyuiopasdfghjklzxcvbnm
```
## Create python virtual environment
```
python3.14 -m venv venv
```
## Activate python virtual environment
```
. venv/bin/activate
```
## Update pip and tools
```
pip install -U pip
pip install --upgrade wheel
pip install --upgrade setuptools
```
## Install dependencies
```
pip install -r requirements.txt
```
### Check syntax
```
ruff check .
```
### Format
```
ruff format .
```
## Run app
```
uvicorn src.main:app --reload --log-config=log_conf.yaml
```
## Run cli application
```
python src/cli.py
```
## Swagger
```
http://127.0.0.1:8000/docs
```
## Redoc
```
http://127.0.0.1:8000/redoc
```
## Test
```
pytest tests/test.py
```
or
```
pytest -s tests/test.py
```
## Docker
```
docker-compose up --build -d
```
```
docker-compose down
```
## Rebuild
´´´
docker-compose up --build -d
´´´