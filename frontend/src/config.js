// window.itvr_config = {
//   "REACT_APP_KEYCLOAK_CLIENT_ID": "itvr-2674",
//   "REACT_APP_KEYCLOAK_REALM": "onestopauth-basic",
//   "REACT_APP_KEYCLOAK_URL": "https://dev.oidc.gov.bc.ca/auth/",
//   "REACT_APP_API_BASE": "https://itvr-backend-dev-102.apps.silver.devops.gov.bc.ca"
// };

export const KEYCLOAK_CLIENT_ID = window.itvr_config
  ? window.itvr_config.REACT_APP_KEYCLOAK_CLIENT_ID
  : process.env.REACT_APP_KEYCLOAK_CLIENT_ID;

export const KEYCLOAK_REALM = window.itvr_config
  ? window.itvr_config.REACT_APP_KEYCLOAK_REALM
  : process.env.REACT_APP_KEYCLOAK_REALM;

export const KEYCLOAK_URL = window.itvr_config
  ? window.itvr_config.REACT_APP_KEYCLOAK_URL
  : process.env.REACT_APP_KEYCLOAK_URL;

export const API_BASE = window.itvr_config
  ? window.itvr_config.REACT_APP_API_BASE
  : process.env.REACT_APP_API_BASE;
