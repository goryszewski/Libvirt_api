#!/bin/bash

docker compose down

docker rm $(docker ps -a --format {{.ID}}) --force
docker compose up  --build
