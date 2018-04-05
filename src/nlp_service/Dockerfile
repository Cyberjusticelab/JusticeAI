FROM python:3

EXPOSE 3002
ARG CJL_USER
ARG CJL_PASS
ENV CJL_USER ${CJL_USER}
ENV CJL_PASS ${CJL_PASS}
ENV FLASK_APP=app.py
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/nlp_service

WORKDIR /usr/src/app

RUN apt-get update -y && apt-get install default-jre -y

RUN mkdir -p /usr/src/app/src/nlp_service/outlier

WORKDIR /usr/src/app/src/nlp_service/outlier

RUN wget --no-check-certificate --user "$CJL_USER" --password "$CJL_PASS" https://capstone.cyberjustice.ca/data/outlier/outlier_estimator.bin.z
RUN wget --no-check-certificate --user "$CJL_USER" --password "$CJL_PASS" https://capstone.cyberjustice.ca/data/outlier/tfidf_vectorizer.bin.z

WORKDIR /usr/src/app

COPY ./src/nlp_service/requirements.txt ./src/nlp_service/
COPY ./src/nlp_service/requirements_test.txt ./src/nlp_service/
RUN pip install -r ./src/nlp_service/requirements_test.txt

# Initialize spacy
RUN python -m spacy download en_core_web_md
RUN python -m spacy link en_core_web_md en

COPY ./src/nlp_service/init_rasa.py ./src/nlp_service
COPY ./src/nlp_service/outlier ./src/nlp_service/outlier
COPY ./src/nlp_service/util ./src/nlp_service/util
COPY ./src/nlp_service/rasa ./src/nlp_service/rasa

# Train RASA classifier
RUN cd src/nlp_service && python init_rasa.py

COPY . .

WORKDIR /usr/src/app/src/nlp_service

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "-p", "3002" ]
