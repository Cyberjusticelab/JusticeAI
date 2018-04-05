FROM python:3

EXPOSE 3003
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/backend_service
ENV FLASK_APP=app.py

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/backend_service

COPY ./src/backend_service/requirements.txt ./src/backend_service/
COPY ./src/backend_service/requirements_test.txt ./src/backend_service/
RUN pip install -r ./src/backend_service/requirements_test.txt

COPY . .

WORKDIR /usr/src/app/src/backend_service

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "-p", "3003" ]
