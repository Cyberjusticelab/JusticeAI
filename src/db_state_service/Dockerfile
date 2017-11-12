FROM python:3

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/db_state_service

COPY ./src/db_state_service/requirements.txt ./src/db_state_service/
COPY ./src/db_state_service/requirements_test.txt ./src/db_state_service/
RUN pip install -r ./src/db_state_service/requirements_test.txt && \
    pip install http://initd.org/psycopg/upload/psycopg2-2.7.3.1.dev0/psycopg2-2.7.3.1.dev0-cp36-cp36m-manylinux1_x86_64.whl

COPY . .

WORKDIR /usr/src/app/src/db_state_service

ENV FLASK_APP=app.py

# TODO: This service to be responsible for DB init & migrations
CMD [ "python3", "-m", "flask", "db", "migrate", "&&", "python3", "-m", "flask", "db", "upgrade" ]

