AWS_ACCESS_KEY_ID ?= AAAAACCESSKEY
AWS_SECRET_ACCESS_KEY ?= SOMEVerySecretKey1234
DEBUG ?= false

.PHONY: run run-nobuild build clean

run:
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) docker-compose up --build

run-nobuild:
	docker-compose pull
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) docker-compose up --no-build

build:
	docker-compse build

clean:
	docker-compose stop
	docker-compose rm

