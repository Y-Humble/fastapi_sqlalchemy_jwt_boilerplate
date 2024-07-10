DC = docker compose
DEV_DC_FILE = docker-compose-dev.yaml
PROD_DC_FILE = docker-compose-prod.yaml
ENV = ./src/environs/.env
ENV_PROD = ./src/environs/.env.prod
ENV_DEV = ./src/environs/.env.dev
ENV_TEST = ./src/environs/.env.test

.PHONY: dev-up dev-down test-up test-down prod-up prod-down show-mode


dev-up:
	sed -i 's/MODE.*/MODE=DEV/' $(ENV)
	$(DC) -f $(DEV_DC_FILE) --env-file $(ENV_DEV) up -d

dev-down:
	$(DC) -f $(DEV_DC_FILE) --env-file $(ENV_DEV) down

test-up:
	sed -i 's/MODE.*/MODE=TEST/' $(ENV)
	$(DC) -f $(DEV_DC_FILE) --env-file $(ENV_TEST) up -d

test-down:
	$(DC) -f $(DEV_DC_FILE) --env-file $(ENV_TEST) down


prod-up:
	sed -i 's/MODE.*/MODE=PROD/' $(ENV)
	$(DC) -f $(PROD_DC_FILE) --env-file $(ENV_PROD) up -d

prod-down:
	$(DC) -f $(PROD_DC_FILE) --env-file $(ENV_PROD) down

show-mode:
	cat $(ENV)
