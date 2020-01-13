## IMGHUB
Image Hub - a small gateway for pictures using simple object storage
- uploading pictures
- list off uploaded pictures with their full url
- delete pictures

The goal is just to play with s3 like storage, flask framework and docker-compose

to test just run `make run-nobuild` - this pulls the image from github docker

to build or build and run `make build` or `make run`

running manually with docker-composer, when deploy, you need to specific to environment variables:
- `AWS_ACCESS_KEY_ID` (running in aws on ecs with a role, leave this blank)
- `AWS_SECRET_ACCESS_KEY` (running in aws on ecs with a role, leave this blank)
- `S3_API_ENDPOINT` (your minio end-point or https://s3.amazonaws.com/ for s3, or equilent for other s3-compatibles)
- `S3_BUCKET` (name of the bucket)
optional:
- `S3_FULL_URL` (full url to your bucket excluding prefix, if other then end-point/bucket)
- `S3_PREFIX` (bucket prefix/folder where images will reside)

- `SESSION_KEY` - a long secret key to signe session cookies with
- `SESSION_TYPE` - the type of session: redis
- `SESSION_REDIS` - the url to redis in form of `redis://url:port`

if you run `make run` it sets them to some default values for local development. access on [http://localhost:5000/listimages]
