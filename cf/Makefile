AWS_PROFILE ?= default
AWS_REGION ?= eu-central-1
TARGET_ENVIRONMENT ?= dev
PROJECT ?= imagehub
GIT_HASH ?= $(shell git describe --long)
DOCKER_IMG_URL ?= docker.pkg.github.com/jakobolsson/imghub/imghub 
FULL_DOMAIN_NAME ?=
SERVICE_NAME ?= imghub
BUCKET_PREFIX ?= images

default:
	@echo "This are the settings:"
	@echo "* Using AWS PROFILE: $(AWS_PROFILE)"
	@echo "* Target Environment: $(TARGET_ENVIRONMENT) (override with TARGET_ENVIRONMENT)"
	@echo "* Target AWS Region: $(AWS_REGION) (override with AWS_REGION)"
	@echo "* Infrastructure bucket: $(BUCKET_NAME) (override with BUCKET_NAME, othwise taken from parameter store)"
	@echo "* Docker Image URL: $(DOCKER_IMG_URL)"
	@echo "* Current Version/GitHash: $(GIT_HASH)"

check-bucket:
	@echo "* * * Checking template bucket $(BUCKET_NAME) exists in $(AWS_REGION)"
	@aws s3api list-buckets --region $(AWS_REGION) --profile $(AWS_PROFILE) | grep -q "$(BUCKET_NAME)" ; \
		if [ $$? -eq 1 ] ; then echo "* * * ERROR: bucket ${BUCKET_NAME} is missing" ; exit 1 ; fi
	@aws ssm get-parameter --name "/region/template-bucket" --region $(AWS_REGION) --profile $(AWS_PROFILE) ; \
		if [ $$? -eq 255 ] ; then echo "* * * ERROR: missing parameter store entry /region/template-bucket" ; exit 1 ; fi
		

upload: BUCKET_NAME := $(shell aws ssm get-parameter --name "/region/template-bucket" --region $(AWS_REGION) --profile $(AWS_PROFILE) --output json | jq -r .Parameter.Value)
upload: SHORT_BUCKET_URL := $(BUCKET_NAME)/$(PROJECT)/$(GIT_HASH)/$(SERVICE_NAME)/
upload: SHORT_BUCKET_URL_LATEST := $(BUCKET_NAME)/$(PROJECT)/latest/$(SERVICE_NAME)/
upload: check-bucket
upload:
	@echo "Uploading files to given bucket $(SHORT_BUCKET_URL)"
	@aws s3 sync . s3://${SHORT_BUCKET_URL} \
		--exclude "*" --include "*.yaml" --include "*.yml" --include "*.json" --delete --region $(AWS_REGION) --profile $(AWS_PROFILE)
	@echo "Also Uploading files to given bucket $(SHORT_BUCKET_URL_LATEST)"
	@aws s3 sync . s3://${SHORT_BUCKET_URL_LATEST} \
		--exclude "*" --include "*.yaml" --include "*.yml" --include "*.json" --delete --region $(AWS_REGION) --profile $(AWS_PROFILE)


create-stack: STACK_NAME := $(TARGET_ENVIRONMENT)-$(SERVICE_NAME) 
create-stack: BUCKET_NAME := $(shell aws ssm get-parameter --name "/region/template-bucket" --region $(AWS_REGION) --profile $(AWS_PROFILE) --output json | jq -r .Parameter.Value)
create-stack: BUCKET_URL := https://s3.amazonaws.com/$(BUCKET_NAME)/$(PROJECT)/$(GIT_HASH)/$(SERVICE_NAME)/
create-stack: PARAMETERS := ParameterKey=EnvironmentName,ParameterValue=$(TARGET_ENVIRONMENT) \
														ParameterKey=Project,ParameterValue=$(PROJECT) \
														ParameterKey=ServiceName,ParameterValue=$(SERVICE_NAME) \
														ParameterKey=Version,ParameterValue=$(GIT_HASH) \
														ParameterKey=DockerImgUrl,ParameterValue=$(DOCKER_IMG_URL) \
														ParameterKey=FullDomainName,ParameterValue=$(FULL_DOMAIN_NAME) \
														ParameterKey=BucketPrefix,ParameterValue=$(BUCKET_PREFIX)
create-stack: upload check-keypair
	@echo "Creating stack $(STACK_NAME)"
	@echo "Tempalte url: $(BUCKET_URL)default.yaml"
	@echo "Parameters: $(PARAMETERS)"
	@echo "* Stack Already exists?: Updating"; \
	 aws cloudformation update-stack --stack-name $(STACK_NAME) \
	 --template-url=$(BUCKET_URL)default.yml \
	 --parameters $(PARAMETERS) \
	 --capabilities CAPABILITY_NAMED_IAM \
	 --region $(AWS_REGION) --profile $(AWS_PROFILE) ; \
	 if [ $$? -eq 255 ] ; then echo "* Stack doesnt exist: Creating" ; \
	 aws cloudformation create-stack --stack-name $(STACK_NAME) \
	 --template-url=$(BUCKET_URL)default.yml \
	 --parameters $(PARAMETERS) \
	 --capabilities CAPABILITY_NAMED_IAM \
	 --region $(AWS_REGION) --profile $(AWS_PROFILE) ; \
	 fi

delete-stack: STACK_NAME := $(TARGET_ENVIRONMENT)-$(SERVICE_NAME) 
delete-stack:
	@aws cloudformation delete-stack --stack-name $(STACK_NAME) \
	 --region $(AWS_REGION) --profile $(AWS_PROFILE)
