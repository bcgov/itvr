import React, { useContext } from 'react';
import Keycloak from 'keycloak-js';

export const bceidKeycloak = new Keycloak({
  clientId: process.env.REACT_APP_BCEID_KEYCLOAK_CLIENT_ID,
  realm: process.env.REACT_APP_BCEID_KEYCLOAK_REALM,
  url: process.env.REACT_APP_BCEID_KEYCLOAK_URL
});

export const bcscKeycloak = new Keycloak({
  clientId: process.env.REACT_APP_BCSC_KEYCLOAK_CLIENT_ID,
  realm: process.env.REACT_APP_BCSC_KEYCLOAK_REALM,
  url: process.env.REACT_APP_BCSC_KEYCLOAK_URL
});

//keycloaks ordered in terms of precedence
export const keycloaks = { bcsc: bcscKeycloak, bceid: bceidKeycloak };

export const KeycloakContext = React.createContext();

export const useKeycloaks = () => {
  const keycloaks = useContext(KeycloakContext);
  return keycloaks;
};

export const useDominantKeycloak = () => {
  let result = null;
  const keycloaks = useKeycloaks();
  for (const i in keycloaks) {
    const keycloak = keycloaks[i];
    if (keycloak.authenticated) {
      result = keycloak;
      break;
    }
  }
  return result;
};
