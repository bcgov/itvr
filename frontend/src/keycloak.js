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

export const addTokenFields = (data, kcToken) => {
  if (data && kcToken) {
    data.first_name = kcToken.given_name;
    data.last_name = kcToken.family_name;
    data.date_of_birth = kcToken.birthdate;
    data.address = kcToken.street_address;
    data.city = kcToken.locality;
    data.postal_code = kcToken.postal_code;
  }
  return data;
};

export const checkBCSC = (kcToken) => {
  const missingBcscfields = [];
  checkField(
    'Your last name (surname)',
    kcToken.family_name,
    missingBcscfields
  );
  checkField('First name (given name)', kcToken.given_name, missingBcscfields);
  checkField('Date of birth', kcToken.birthdate, missingBcscfields);
  checkField('Street address', kcToken.street_address, missingBcscfields);
  checkField('City', kcToken.locality, missingBcscfields);
  return missingBcscfields;
};

export const checkField = (name, answer, missingBcscfields) => {
  if (!answer) {
    missingBcscfields.push(name);
  }
};
