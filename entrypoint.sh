#!/bin/bash

psql --username "$POSTGRES_USER" <<-EOSQL
    CREATE USER taskuser WITH PASSWORD 'admin';
    CREATE DATABASE task_db;
    \c task_db;
    GRANT ALL PRIVILEGES ON DATABASE task_db TO taskuser;
    GRANT ALL ON ALL TABLES IN SCHEMA public TO taskuser;
    GRANT ALL ON ALL SEQUENCES IN SCHEMA public TO taskuser;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON TABLES TO taskuser;
    ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT ALL ON SEQUENCES TO taskuser;
EOSQL

python /app/main/manage.py makemigrations
python /app/main/manage.py migrate