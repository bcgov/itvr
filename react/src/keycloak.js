import Keycloak from 'keycloak-js';

const keycloak = new Keycloak({
  clientId: 'itvr-2674',
  realm: 'onestopauth-basic',
  url: 'https://dev.oidc.gov.bc.ca/auth',
});

export default keycloak;

// // Setup Keycloak instance as needed
// // Pass initialization options as required or leave blank to load from 'keycloak.json'
// const keycloak = Keycloak({
//   url: 'http://localhost:8080/auth',
//   realm: 'Test',
//   clientId: 'react-test',
// });

// export default keycloak;

// {
//   "confidential-port": 0,
//   "auth-server-url": "https://dev.oidc.gov.bc.ca/auth",
//   "realm": "onestopauth-basic",
//   "ssl-required": "external",
//   "public-client": true,
//   "resource": "itvr-2674"
// }