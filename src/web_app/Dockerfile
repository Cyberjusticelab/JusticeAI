FROM node:latest

WORKDIR /usr/src/app

RUN apt-get install git -y

COPY . .

RUN npm install

EXPOSE 3039
ENV PORT=3039
CMD [ "npm", "start"]
