# syntax=docker/dockerfile:1

FROM python:3.8
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN pip3 install -e ./src/
ENTRYPOINT ["/usr/local/bin/cis-integration"]
