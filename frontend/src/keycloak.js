import Keycloak from 'keycloak-js';
import { KEYCLOAK_CLIENT_ID, KEYCLOAK_REALM, KEYCLOAK_URL } from './config';

const keycloak = new Keycloak({
  clientId: KEYCLOAK_CLIENT_ID,
  realm: KEYCLOAK_REALM,
  url: KEYCLOAK_URL
});

export default keycloak;
