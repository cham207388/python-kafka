.PHONY: help dcu dcd app server consumer migrate revision path sleep5 setup

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

app: migrate
	poetry run uvicorn src.server:app --reload

consumer: migrate ## start consumer group
	poetry run python src/consumer/main.py

migrate: ## alembic migration
	poetry run alembic upgrade head

revision: ## make revision message='custom message'
	poetry run alembic revision -m $(message)

dcu: ## start kafka cluster 3 brokers
	docker compose -f compose-3b.yaml up --build -d

dcd: ## stop kafka cluster 3 brokers
	docker compose -f compose-3b.yaml down -v

path:
	poetry env info --path

sleep5:
	sleep 5

setup: dcu sleep5 migrate
	echo "start docker and alembic migrate"