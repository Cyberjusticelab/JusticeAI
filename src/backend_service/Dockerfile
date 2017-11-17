FROM python:3

EXPOSE 3003
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/backend_service
ENV FLASK_APP=app.py

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/backend_service

COPY ./src/backend_service/requirements.txt ./src/backend_service/
COPY ./src/backend_service/requirements_test.txt ./src/backend_service/
RUN pip install http://initd.org/psycopg/upload/psycopg2-2.7.3.1.dev0/psycopg2-2.7.3.1.dev0-cp36-cp36m-manylinux1_x86_64.whl && \
    pip install -r ./src/backend_service/requirements_test.txt

COPY . .

WORKDIR /usr/src/app/src/backend_service

CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:3003", "app:app" ]
