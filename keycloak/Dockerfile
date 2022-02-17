FROM jboss/keycloak:latest

COPY realm.json /tmp/realm.json
ENV KEYCLOAK_IMPORT /tmp/realm.json

RUN /opt/jboss/keycloak/bin/add-user-keycloak.sh -r Demo -u user -p 1234
