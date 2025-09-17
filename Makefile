# makefile
DC = docker compose
EXEC = docker exec -it
LOGS = docker logs
ENV = --env-file .env
APP_FILE = docker_compose_local.yaml
STORAGES_FILE = docker_compose/storages.yaml
APP_CONTAINER = app


.PHONY: app-local
app-local:
	@uv run -m src.main

.PHONY: app
app:
	@${DC} -f ${APP_FILE} up --build -d

.PHONY: app-down
app-down:
	@${DC} -f ${APP_FILE} down
