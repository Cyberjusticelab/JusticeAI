FROM python:3

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/nlp_service

COPY ./src/nlp_service/requirements.txt ./src/nlp_service/
COPY ./src/nlp_service/requirements_test.txt ./src/nlp_service/
RUN pip install -r ./src/nlp_service/requirements_test.txt

COPY . .
RUN cd src/nlp_service && python init.py

WORKDIR /usr/src/app/src/nlp_service

ENV FLASK_APP=app.py
EXPOSE 3002
CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:3002", "app:app" ]
