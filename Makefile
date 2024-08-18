SERVICES := qdrant db

.PHONY: local
local:
	@uvicorn reviewturtl.api.api:app --proxy-headers --host 127.0.0.1 --port 7001 --log-level debug --reload --timeout-keep-alive 65

# Default target: start services
.PHONY: all
all: up

# Start all services
.PHONY: up
up:
	@if [ -z "$(filter-out up,$(MAKECMDGOALS))" ]; then \
		docker-compose up -d $(SERVICES); \
	else \
		docker-compose up -d $(filter-out $@,$(MAKECMDGOALS)); \
	fi

# Stop all services
.PHONY: down
down:
	@if [ -z "$(filter-out down,$(MAKECMDGOALS))" ]; then \
		docker-compose down $(SERVICES); \
	else \
		docker-compose down $(filter-out $@,$(MAKECMDGOALS)); \
	fi
