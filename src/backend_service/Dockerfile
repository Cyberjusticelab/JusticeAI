FROM python:3

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/backend_service

COPY ./src/backend_service/requirements.txt ./src/backend_service/
COPY ./src/backend_service/requirements_test.txt ./src/backend_service/
RUN pip install --no-cache-dir -r ./src/backend_service/requirements_test.txt

COPY . .

WORKDIR /usr/src/app/src/backend_service

ENV FLASK_APP=app.py
EXPOSE 3003
CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:3003", "app:app" ]
