FROM node:14

WORKDIR /web

COPY package*.json /web/
RUN npm install

COPY . .

EXPOSE 3000
