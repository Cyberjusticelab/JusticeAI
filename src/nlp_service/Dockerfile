FROM python:3

EXPOSE 3002
ENV FLASK_APP=app.py
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/nlp_service

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/nlp_service/outlier

COPY ./src/nlp_service/requirements.txt ./src/nlp_service/
COPY ./src/nlp_service/requirements_test.txt ./src/nlp_service/
RUN pip install http://initd.org/psycopg/upload/psycopg2-2.7.3.1.dev0/psycopg2-2.7.3.1.dev0-cp36-cp36m-manylinux1_x86_64.whl && \
    pip install -r ./src/nlp_service/requirements_test.txt

# Initialize spacy
RUN python -m spacy download en

COPY ./src/nlp_service/init_rasa.py ./src/nlp_service
COPY ./src/nlp_service/outlier ./src/nlp_service/outlier
COPY ./src/nlp_service/rasa ./src/nlp_service/rasa

# Train RASA classifier
RUN cd src/nlp_service && python init_rasa.py

COPY . .

WORKDIR /usr/src/app/src/nlp_service

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "-p", "3002" ]
