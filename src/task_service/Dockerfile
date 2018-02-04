FROM base/archlinux:latest

EXPOSE 3004
ARG CJL_USER
ARG CJL_PASS
ENV CJL_USER ${CJL_USER}
ENV CJL_PASS ${CJL_PASS}
ENV FLASK_APP=app.py
ENV PYTHONPATH /usr/src/app/src:/usr/src/app/src/task_service

WORKDIR /usr/src/app
RUN echo 'en_US.UTF-8 UTF-8' > /etc/locale.gen  && \
    echo 'LANG=en_US.UTF-8' > /etc/locale.conf && \
    locale-gen && \
    unset LANG

ENV LC_ALL en_US.utf-8
ENV LANG en_US.utf-8

RUN pacman -Syyu --noconfirm && \
  pacman -S --noconfirm \
    python3 \
    python-pip \
    gcc \
    tesseract\
    tesseract-data-eng \
    tesseract-data-fra \
    opencv

COPY ./src/task_service/requirements.txt ./src/task_service/
COPY ./src/task_service/requirements_test.txt ./src/task_service/
RUN pip install -r ./src/task_service/requirements_test.txt

COPY . .

WORKDIR /usr/src/app/src/task_service

CMD [ "python", "-m", "flask", "run", "--host", "0.0.0.0", "-p", "3004" ]
