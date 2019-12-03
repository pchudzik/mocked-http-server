FROM python:3.7-slim

RUN mkdir /app

ENV PORT=80
ENV ERROR_RATIO=0.1
ENV ERROR_FILE=error.json
ENV SUCCESS_FILE=success.json
ENV PATH=/api

COPY . /app/

WORKDIR /app

EXPOSE 80

CMD /usr/local/bin/python3 server.py \
    --port=$PORT \
    --error-ratio=$ERROR_RATIO \
    --error-file=$ERROR_FILE \
    --success-file=$SUCCESS_FILE \
    --path=$PATH
