include ./src/.env
export

all: up

up: build
	docker compose -f ./docker/docker-compose.yml -p plnd4u up -d

build:
	docker build -t plnd4u-image .

down:
	docker compose -f ./docker/docker-compose.yml -p plnd4u down

deploy:
	ansible-playbook ./docker/playbook-up.yaml

destroy:
	ansible-playbook ./docker/playbook-down.yaml

db-term:
	docker exec -it plnd4u-db-1 bash

mysql-remote:
	mysql -h dev.plnd4u.com -P 3306 -u root -p

dump:
	docker exec plnd4u-db-1 /bin/bash -c "mysql -u root -p plnd4u < /mnt/data/dump.sql"

db-clean:
	python3 src/clean_db.py

restart: down
	docker compose -f ./docker/docker-compose.yml -p plnd4u up -d

db-sql:
#	docker exec plnd4u-db-1 -it /bin/mysql -c "--password=$MYSQL_ROOT_PASSWORD --database=plnd4u"

configure: up
	@echo "Waiting..."
	@sleep 5
	docker exec plnd4u-db-1 mysql --password=$$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE plnd4u;" || true
	@echo "Waiting..."
	@sleep 3
	docker exec plnd4u-db-1 sh -c 'mysql -u root --password=$$MYSQL_ROOT_PASSWORD plnd4u < /mnt/data/dump2.sql'
	
test:
	docker exec plnd4u-db-1 sh -c 'cat /mnt/data/dump.sql'
