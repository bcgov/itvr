FROM --platform=linux/amd64 node:16

WORKDIR /web

COPY package*.json /web/
RUN npm install

COPY . .

EXPOSE 3000
