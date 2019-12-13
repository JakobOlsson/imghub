AWS_ACCESS_KEY_ID ?= AAAAACCESSKEY
AWS_SECRET_ACCESS_KEY ?= SOMEVerySecretKey1234
DEBUG ?= false
GIT_HASH ?= $(shell git describe --long)
DOCKER_IMG_URL ?= docker.pkg.github.com/jakobolsson/imghub/imghub

.PHONY: run run-nobuild build clean

run:
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) DOCKER_IMG_URL=$(DOCKER_IMG_URL) docker-compose up --build

run-nobuild:
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) DOCKER_IMG_URL=$(DOCKER_IMG_URL) docker-compose up --no-build

build:
	AWS_ACCESS_KEY_ID=$(AWS_ACCESS_KEY_ID) AWS_SECRET_ACCESS_KEY=$(AWS_SECRET_ACCESS_KEY) DOCKER_IMG_URL=$(DOCKER_IMG_URL) docker-compose build

push: build
	docker tag $(DOCKER_IMG_URL):latest $(DOCKER_IMG_URL):$(GIT_HASH)
	docker push $(DOCKER_IMG_URL):$(GIT_HASH)
	docker push $(DOCKER_IMG_URL):latest

clean:
	docker-compose stop
	docker-compose rm

