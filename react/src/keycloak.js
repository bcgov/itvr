import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  clientId: 'itvr-2674',
  realm: 'onestopauth-basic',
  url: 'https://dev.oidc.gov.bc.ca/auth',
});

export default keycloak;
