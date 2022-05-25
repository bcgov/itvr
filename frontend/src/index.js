import React from 'react';
import ReactDOM from 'react-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import AppRouter from './routes';
import { KeycloakProvider, bcscKeycloak, bceidKeycloak } from './keycloak';
import './styles/index.scss';

const queryClient = new QueryClient();

const initOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
};

const keycloaks = { bcsc: bcscKeycloak, bceid: bceidKeycloak };

ReactDOM.render(
  <KeycloakProvider
    authClient={keycloaks}
    initOptions={initOptions}
    LoadingComponent={<div>Loading</div>}
  >
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  </KeycloakProvider>,
  document.getElementById('root')
);
