.PHONY: clean build run re

clean:
	docker compose down
	-docker rm $(shell docker ps -a --format {{.ID}}) --force

build:
	docker compose build

run:
	docker compose down
	docker compose up



re: clean build run
