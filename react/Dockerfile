FROM node:16

RUN mkdir /web && chown node:node /web

WORKDIR /web

COPY --chown=node:node package.json package-lock.json* ./
USER node
RUN npm install --legacy-peer-deps && npm cache clean --force

COPY --chown=node:node . .

EXPOSE 3000
