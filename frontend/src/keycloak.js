import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  clientId: process.env.REACT_APP_KEYCLOAK_CLIENT_ID,
  realm: process.env.REACT_APP_KEYCLOAK_REALM,
  url: process.env.REACT_APP_KEYCLOAK_URL,
});

export default keycloak;
