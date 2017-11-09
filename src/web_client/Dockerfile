FROM node:8.9.0

WORKDIR /usr/src/app

RUN mkdir -p /usr/src/app/src/web_client

RUN apt-get install git -y

COPY . .

WORKDIR /usr/src/app/src/web_client

RUN npm install


EXPOSE 3039
ENV PORT=3039
CMD [ "npm", "start"]
