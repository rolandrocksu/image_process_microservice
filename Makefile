build:
	@docker build -t hr-tool:local .

run: build
	@docker run -it --rm --name hr-tool -p 8000:8000 -v $(shell pwd):/usr/src/app hr-tool:local

migrate:
	@docker exec -it hr-tool python manage.py migrate

exec:
	@docker exec -it hr-tool bash
