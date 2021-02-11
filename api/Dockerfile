# Stage 0 - Gunicorn server
FROM python:3.7.3-slim as gunicorn-stage
COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt
COPY ./ /app/api
WORKDIR /app/api
ENTRYPOINT ["./gunicorn_starter.sh"]