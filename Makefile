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
	

