FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .
RUN python init.py

ENV FLASK_APP=app.py
EXPOSE 3001
CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:3001", "app:app" ]
