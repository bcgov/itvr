FROM node:16

RUN mkdir /usr/src/app && chown node:node /usr/src/app

WORKDIR /usr/src/app

COPY --chown=node:node package.json package-lock.json* ./
USER node
RUN npm install --legacy-peer-deps && npm cache clean --force

COPY --chown=node:node . .

EXPOSE 3000
