# Stage 0 - Gunicorn server
FROM python:3.7.3-slim as gunicorn-stage
COPY ./requirements.txt /
RUN pip3 install -r /requirements.txt
COPY ./ /app/api
RUN mkdir /root/.aws/
COPY ./secret/awscredentials /root/.aws/credentials
COPY ./awsconfig /root/.aws/config
WORKDIR /app/api
RUN chmod +x gunicorn_starter.sh

ENTRYPOINT ["./gunicorn_starter.sh"]