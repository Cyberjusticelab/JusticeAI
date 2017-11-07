FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
COPY requirements_test.txt ./
RUN pip install --no-cache-dir -r requirements_test.txt

COPY . .

# Initialize spacy
RUN python -m spacy download en

# Initialize Flask App
ENV FLASK_APP=app.py
EXPOSE 3002
CMD [ "gunicorn", "-w 3", "-b 0.0.0.0:3002", "app:app" ]
