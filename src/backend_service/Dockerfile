FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 3003
CMD [ "gunicorn", "-w 3", "--reload", "-b 0.0.0.0:3003", "app:app" ]
