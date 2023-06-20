run: ## Run the test server.
	python manage.py runserver_plus

install: ## Install the python requirements.
	pip install -r requirements.txt

migrate: ## Make migrations
	python manage.py migrate

makemigrations: ## Generate database migrations from models state
	python manage.py makemigrations

shell: ## Open python shell with settings.py path provided to Django
	python manage.py shell

collectstatic: ## Store all needed static files for display
	python manage.py collectstatic