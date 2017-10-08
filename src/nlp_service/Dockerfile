FROM python:3

WORKDIR /usr/src/app

COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

RUN python init.py
RUN python data_augmenter.py
ENV FLASK_APP=app.py
EXPOSE 3002
CMD [ "python", "-m", "flask", "run", "--host=0.0.0.0", "-p 3002" ]
