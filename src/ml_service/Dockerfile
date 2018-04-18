FROM python:3

EXPOSE 3001
ARG CJL_USER
ARG CJL_PASS
ENV CJL_USER ${CJL_USER}
ENV CJL_PASS ${CJL_PASS}
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/ml_service
ENV FLASK_APP=app.py

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/ml_service/data/binary/

COPY ./src/ml_service/requirements.txt ./src/ml_service/
COPY ./src/ml_service/requirements_test.txt ./src/ml_service/
RUN pip install -r ./src/ml_service/requirements_test.txt

COPY ./src/ml_service/init.py ./src/ml_service/
COPY ./src/ml_service/util/* ./src/ml_service/util/
RUN cd src/ml_service && python init.py

COPY . .


WORKDIR /usr/src/app/src/ml_service

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "-p", "3001" ]
