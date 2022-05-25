import React, { useState, useEffect, useContext } from 'react';
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

const KeycloakContext = React.createContext();

//authClient is an object of keycloaks, ordered by precedence (i.e. an authClient of {bcscKeycloak, bceidKeycloak}
//implies that if the user is logged in as both a bcsc and bceid user, the useDominantAuthenticatedKeycloak() hook will return the bcsc keycloak)
export const KeycloakProvider = ({
  children,
  authClient,
  initOptions,
  LoadingComponent
}) => {
  const [
    keycloaksSuccessfullyInitialized,
    setKeycloaksSuccessfullyInitialized
  ] = useState(false);
  const [
    keycloaksUnsuccessfullyInitialized,
    setKeycloaksUnsuccessfullyInitialized
  ] = useState(false);
  useEffect(() => {
    const keycloakPromises = [];
    for (const i in authClient) {
      const keycloak = authClient[i];
      keycloakPromises.push(keycloak.init(initOptions));
    }
    Promise.all(keycloakPromises)
      .then(() => {
        setKeycloaksSuccessfullyInitialized(true);
      })
      .catch(() => {
        setKeycloaksUnsuccessfullyInitialized(true);
      });
  }, []);
  if (keycloaksSuccessfullyInitialized || keycloaksUnsuccessfullyInitialized) {
    const value = {
      keycloaks: authClient,
      initialized: keycloaksSuccessfullyInitialized
    };
    return (
      <KeycloakContext.Provider value={value}>
        {children}
      </KeycloakContext.Provider>
    );
  }
  return LoadingComponent;
};

export const useKeycloaks = () => {
  return useContext(KeycloakContext);
};

export const useDominantAuthenticatedKeycloak = () => {
  let result = null;
  const { keycloaks, initialized } = useKeycloaks();
  if (initialized) {
    for (const i in keycloaks) {
      const keycloak = keycloaks[i];
      if (keycloak.authenticated) {
        result = keycloak;
        break;
      }
    }
  }
  return result;
};
