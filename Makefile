.PHONY: help dcu dcd dcall dcdown dc3 dcd3 produce server consumer migrate revision

message=""

help: ## Show this help message with aligned shortcuts, descriptions, and commands
	@awk 'BEGIN {FS = ":"; printf "\033[1m%-20s %-40s %s\033[0m\n", "Target", "Description", "Command"} \
	/^[a-zA-Z_-]+:/ { \
		target=$$1; \
		desc=""; cmd="(no command)"; \
		if ($$2 ~ /##/) { sub(/^.*## /, "", $$2); desc=$$2; } \
		getline; \
		if ($$0 ~ /^(\t|@)/) { cmd=$$0; sub(/^(\t|@)/, "", cmd); } \
		printf "%-20s %-40s %s\n", target, desc, cmd; \
	}' $(MAKEFILE_LIST)

dcu: ## Start Kafka cluster
	docker compose -f ./compose.yaml up -d

dcd: ## Stop Kafka cluster
	docker compose -f ./compose.yaml down -v
	
dcall: ## start kafka cluster
	docker compose -f confluent-compose.yaml up -d
	
dcdown: ## stop kafka cluster
	docker compose -f confluent-compose.yaml down -v
  
produce: ## producer script
	poetry run python producer/main.py

server: ## producer fast api
	poetry run uvicorn producer.server:app --reload
	
consumer: ## start consumer group
	poetry run python consumer/main.py
	
migrate: ## alembic migration
	poetry run alembic upgrade head
	
revision: ## make revision message='custom message'
	poetry run alembic revision -m $(message)
	
dc3: ## start kafka cluster 3 brokers
	docker compose -f confluent-compose-3b.yaml up -d
	
dcd3: ## stop kafka cluster 3 brokers
	docker compose -f confluent-compose-3b.yaml down -v

sleep:
	sleep 5

path:
	poetry env info --path