
clean:
	docker compose down
	docker rm $(shell docker ps -a --format {{.ID}}) --force | exit 0

up:
	docker compose up  --build

re: clean up
