FROM python:3
ARG CJL_USER
ARG CJL_PASS
WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/ml_service

COPY ./src/ml_service/requirements.txt ./src/ml_service/
COPY ./src/ml_service/requirements_test.txt ./src/ml_service/
RUN pip install --no-cache-dir -r ./src/ml_service/requirements_test.txt

COPY . .

ENV CJL_USER ${CJL_USER}
ENV CJL_PASS ${CJL_PASS}
RUN cd src/ml_service && python init.py

WORKDIR /usr/src/app/src/ml_service

ENV FLASK_APP=app.py
EXPOSE 3001
CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:3001", "app:app" ]