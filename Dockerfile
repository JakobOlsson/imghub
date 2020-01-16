FROM python:3.7-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/app/ /app

ENV FLASK_ENV="development"
ENV FLASK_APP="imghub"
ENV DEBUG="false"
ENV AWS_ACCESS_KEY_ID=""
ENV AWS_SECRET_ACCESS_KEY=""
ENV S3_PREFIX="images"
ENV S3_BUCKET="imagebucket"
ENV S3_API_ENDPOINT="http://localhost:9000"
ENV S3_FULL_URL=""
ENV SESSION_TYPE="redis"
ENV SESSION_KEY=""

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
