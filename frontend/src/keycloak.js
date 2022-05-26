import Keycloak from 'keycloak-js';

export const bcscRealm = process.env.REACT_APP_BCSC_KEYCLOAK_REALM;
export const bceidRealm = process.env.REACT_APP_BCEID_KEYCLOAK_REALM;

const bcscKeycloak = new Keycloak({
  clientId: process.env.REACT_APP_BCSC_KEYCLOAK_CLIENT_ID,
  realm: bcscRealm,
  url: process.env.REACT_APP_BCSC_KEYCLOAK_URL
});

const bceidKeycloak = new Keycloak({
  clientId: process.env.REACT_APP_BCEID_KEYCLOAK_CLIENT_ID,
  realm: bceidRealm,
  url: process.env.REACT_APP_BCEID_KEYCLOAK_URL
});

export const keycloakInitOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
};

export const keycloaks = {
  [bcscRealm]: bcscKeycloak,
  [bceidRealm]: bceidKeycloak
};
