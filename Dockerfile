# syntax=docker/dockerfile:1

FROM python:3.9
WORKDIR /app
COPY requirements.txt requirements.txt
RUN pip3 install -r requirements.txt
COPY . .
<<<<<<< HEAD
RUN python3 setup.py install
RUN adduser -u 5678 --disabled-password --gecos "" appuser && chown -R appuser /app
USER appuser
=======
RUN pip3 install -e ./src/ -t /usr/local/bin/
>>>>>>> 5c560c0 (update to dockerfile)
CMD [ "bash" ]