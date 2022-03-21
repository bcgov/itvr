import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';

import keycloak from './keycloak';
import AppRouter from './routes';

import './styles/index.scss';

const eventLogger = (event, error) => {
  console.log('onKeycloakEvent', event, error);
};

const tokenLogger = (tokens) => {
  console.log('onKeycloakTokens', tokens);
};

const initOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
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
  document.getElementById('root')
);
