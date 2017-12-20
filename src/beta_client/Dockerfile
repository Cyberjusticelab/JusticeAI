FROM node:8.9.0

EXPOSE 3039
ENV PORT=3039

RUN apt-get install git -y

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/web_client

COPY ./src/web_client/package.json ./src/web_client/

RUN cd ./src/web_client && npm install

COPY . .

WORKDIR /usr/src/app/src/web_client

CMD [ "npm", "start"]
