FROM python:3

EXPOSE 3004
ARG CJL_USER
ARG CJL_PASS
ENV CJL_USER ${CJL_USER}
ENV CJL_PASS ${CJL_PASS}
ENV FLASK_APP=app.py
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/ocr_service

WORKDIR /usr/src/app

COPY ./src/ocr_service/requirements.txt ./src/ocr_service/
COPY ./src/ocr_service/requirements_test.txt ./src/ocr_service/
RUN pip install http://initd.org/psycopg/upload/psycopg2-2.7.3.1.dev0/psycopg2-2.7.3.1.dev0-cp36-cp36m-manylinux1_x86_64.whl && \
    pip install -r ./src/ocr_service/requirements_test.txt

COPY . .

WORKDIR /usr/src/app/src/ocr_service

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "-p", "3004" ]
