FROM python:3

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/db_state_service

COPY ./src/db_state_service/requirements.txt ./src/db_state_service/
COPY ./src/db_state_service/requirements_test.txt ./src/db_state_service/
RUN pip install -r ./src/db_state_service/requirements_test.txt

COPY . .

WORKDIR /usr/src/app/src/db_state_service

ENV FLASK_APP=app.py

# TODO: This service to be responsible for DB init & migrations
CMD [ "flask db init" ]

