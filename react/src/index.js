import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';

import keycloak from './keycloak';
import settings from './settings';

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

if (settings.ENABLE_KEYCLOAK) {
  ReactDOM.render(
    <ReactKeycloakProvider
      authClient={keycloak}
      onEvent={eventLogger}
      onTokens={tokenLogger}
      initOptions={initOptions}
    >
      <AppRouter />
    </ReactKeycloakProvider>,
    document.getElementById('root'),
  );
} else {
  ReactDOM.render(<AppRouter />, document.getElementById('root'));
}
