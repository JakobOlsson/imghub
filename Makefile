AWS_ACCESS_KEY_ID ?= AAAAACCESSKEY
AWS_SECRET_ACCESS_KEY ?= SOMEVerySecretKey1234

.PHONY: run

run:
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) docker-compose up --build

build:
	docker-compse build

clean:
	docker-compose stop
	docker-compose rm

