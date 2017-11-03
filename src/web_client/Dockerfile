FROM node:8.9.0

WORKDIR /usr/src/app

RUN apt-get install git -y

COPY package.json .
RUN npm install

COPY . .

EXPOSE 3039
ENV PORT=3039
CMD [ "npm", "start"]
