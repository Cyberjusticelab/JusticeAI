FROM python:3

WORKDIR /usr/src/app

COPY . .

WORKDIR /usr/src/app/src/db_state_service

# TODO: This service to be responsible for DB init & migrations
# For now, just run arbitrary command
CMD [ "pwd" ]

