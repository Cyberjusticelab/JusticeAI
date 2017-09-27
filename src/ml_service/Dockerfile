FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

ENV FLASK_APP=app.py
EXPOSE 3001
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "-p 3001" ]
