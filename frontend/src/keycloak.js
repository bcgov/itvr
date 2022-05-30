import Keycloak from 'keycloak-js';
import {
  BCEID_KEYCLOAK_CLIENT_ID,
  BCEID_KEYCLOAK_REALM,
  BCEID_KEYCLOAK_URL,
  BCSC_KEYCLOAK_CLIENT_ID,
  BCSC_KEYCLOAK_REALM,
  BCSC_KEYCLOAK_URL
} from './config';

const bcscKeycloak = new Keycloak({
  clientId: BCSC_KEYCLOAK_CLIENT_ID,
  realm: BCSC_KEYCLOAK_REALM,
  url: BCSC_KEYCLOAK_URL
});

const bceidKeycloak = new Keycloak({
  clientId: BCEID_KEYCLOAK_CLIENT_ID,
  realm: BCEID_KEYCLOAK_REALM,
  url: BCEID_KEYCLOAK_URL
});

export const keycloakInitOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
};

export const keycloaks = {
  [BCSC_KEYCLOAK_REALM]: bcscKeycloak,
  [BCEID_KEYCLOAK_REALM]: bceidKeycloak
};

export const getKeycloak = () => {
  const realm = localStorage.getItem('keycloakRealm');
  if (realm) {
    return keycloaks[realm];
  }
  return keycloaks[BCSC_KEYCLOAK_REALM];
};
