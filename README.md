## IMGHUB
Image Hub - a small gateway for pictures using simple object storage
- uploading pictures
- list off uploaded pictures with their full url
- delete pictures

The goal is just to play with s3 like storage, flask framework and docker-compose

to test just run `make run-nobuild` - this pulls the image from github docker

to build or build and run `make build` or `make run`

running manually with docker-composer, when deploy, you need to specific to environment variables:
- `AWS_ACCESS_KEY_ID`
- `AWS_SECRET_ACCESS_KEY`
- `S3_URL`
- `S3_BUCKET`

if you run `make run` it sets them to some default values for local development
