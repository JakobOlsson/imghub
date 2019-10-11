FROM python:3.7-alpine

COPY ./requirements.txt /app/requirements.txt

WORKDIR /app

RUN pip install --no-cache-dir -r requirements.txt

COPY ./src/app/ /app

ENTRYPOINT [ "python" ]

CMD [ "server.py" ]
