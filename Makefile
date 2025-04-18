.PHONY: help dcu dcd



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