FROM node:latest

WORKDIR /usr/src/app

RUN apt-get install git -y

COPY .codecov.yml .
COPY src/web_app .

RUN npm install

EXPOSE 3000
ENV PORT=3000
CMD [ "npm", "start"]
