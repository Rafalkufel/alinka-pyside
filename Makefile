APP_VERSION=$(shell docker-compose run app poetry version --short)
INSTALLER_FILE_NAME="alinka-$(APP_VERSION).deb"

help: ## Show this help
	@grep -E '^[a-zA-Z_-]+:.*?## .*$$' $(MAKEFILE_LIST) | sort | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-20s\033[0m %s\n", $$1, $$2}'


test: ## Run all unit tests
	docker-compose run app pytest .

build: ## Build docker image
	docker-compose build --no-cache

run: ## Run application
	docker-compose run app python app/main.py

type=specjalne
generate: ## Generate documents. Use `type=` params to create given type of document.
	docker-compose run app python app/create_documents.py --type ${type}

style: ## Run black, isort, flake8 linters
	docker-compose run app bash -c "black . && isort . && flake8 ."

style-check:
	docker-compose run app bash -c "black . --check && isort . --check && flake8 ."

installer: ## Create installer
	docker-compose run -u root app pyinstaller alinka.spec --noconfirm
	docker-compose run -u root app ./package.sh
	docker-compose run -u root app fpm -v $(APP_VERSION) -p $(INSTALLER_FILE_NAME)

installer-name: ## Display name of installer of current version of app
	@echo $(INSTALLER_FILE_NAME)
