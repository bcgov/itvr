import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';

import keycloak from './keycloak';

import './styles/index.scss';

import AppRouter from './routes';

const eventLogger = (event, error) => {
  console.log('onKeycloakEvent', event, error);
};

const tokenLogger = (tokens) => {
  console.log('onKeycloakTokens', tokens);
};

const initOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256',
  redirectUri: `${window.location.origin}/`,
};

ReactDOM.render(
  <ReactKeycloakProvider
    authClient={keycloak}
    onEvent={eventLogger}
    onTokens={tokenLogger}
    initOptions={initOptions}
    LoadingComponent={<div>Loading</div>}
  >
    <AppRouter />
  </ReactKeycloakProvider>,
  document.getElementById('root'),
);
