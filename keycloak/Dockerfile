FROM jboss/keycloak:latest

COPY realm.json /tmp/realm.json

ENV KEYCLOAK_USER admin
ENV KEYCLOAK_PASSWORD admin

ENV KEYCLOAK_IMPORT /tmp/realm.json
ARG KEYCLOAK_FRONTEND_URL=${KEYCLOAK_FRONTEND_URL}
ENV KEYCLOAK_FRONTEND_URL ${KEYCLOAK_FRONTEND_URL}

RUN /opt/jboss/keycloak/bin/add-user-keycloak.sh -r Demo -u user -p 1234