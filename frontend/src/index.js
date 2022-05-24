import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import { QueryClient, QueryClientProvider } from 'react-query';
import keycloak from './keycloak';
import AppRouter from './routes';

import './styles/index.scss';

const queryClient = new QueryClient();

const initOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256',
  useNonce: false
};

ReactDOM.render(
  <ReactKeycloakProvider
    authClient={keycloak}
    initOptions={initOptions}
  >
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  </ReactKeycloakProvider>,
  document.getElementById('root')
);
