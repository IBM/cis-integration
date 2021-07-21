# syntax=docker/dockerfile:1

FROM python:3.9
ENV PYTHONPATH="."
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
RUN python3 setup.py install
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
CMD [ "bash" ]