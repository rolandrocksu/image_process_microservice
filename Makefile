build:
	@docker build -t image-process:local .

run: build
	@docker run -it --rm --name image-process -p 8000:8000 -v $(shell pwd):/usr/src/app image-process:local

migrate:
	@docker exec -it image-process python manage.py migrate

exec:
	@docker exec -it image-process bash
