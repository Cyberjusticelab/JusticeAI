FROM node:latest

WORKDIR /usr/src/app

COPY . .

RUN npm install

EXPOSE 3000
ENV PORT=3000
CMD [ "npm", "start"]
