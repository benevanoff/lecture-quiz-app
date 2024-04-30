# How to..

## Start Docker

1. Open Docker Desktop App
2. Go to /infrastructure
3. Write: docker compose up --build

## Get into Database

1. Go to /infrastructure
2. Write: docker exec -it infrastructure-db_mysql-1 /bin/sh
3. Write: mysql -u root -p sql_db
4. Pasdword: sqlpasswordsql
