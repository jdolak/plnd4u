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
	docker exec plnd4u-db-1 sh -c "mysql -u root -p plnd4u < /mnt/data/dump.sql"

db-clean:
	python3 src/clean_db.py

restart: down
	docker compose -f ./docker/docker-compose.yml -p plnd4u up -d

db-sql:
	docker exec plnd4u-db-1 sh -tic "mysql --password=$$MYSQL_ROOT_PASSWORD --database=plnd4u"

configure: up
	@echo "Waiting..."
	@sleep 5
	docker exec plnd4u-db-1 mysql --password=$$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE plnd4u;" || true
	@echo "Waiting..."
	@sleep 3
	docker exec plnd4u-db-1 sh -c 'mysql -u root --password=$$MYSQL_ROOT_PASSWORD plnd4u < /mnt/data/dump.sql'
	
test: build
	@docker compose -f ./docker/docker-compose.yml -p plnd4u up -d
	@echo "Creating test environment..."
	@sleep 7
	@docker exec plnd4u-db-1 mysql --password=$$MYSQL_ROOT_PASSWORD -e "CREATE DATABASE plnd4u;" 2> /dev/null || true
	@echo "Uploading data..."
	@sleep 3
	@docker exec plnd4u-db-1 sh -c 'mysql -u root --password=$$MYSQL_ROOT_PASSWORD plnd4u < /mnt/data/dump.sql' 2> /dev/null
	@echo "Running unit tests..."
	@python3 ./tests/integration-tests.py

