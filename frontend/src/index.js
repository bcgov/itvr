import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import { QueryClient, QueryClientProvider } from 'react-query';
import { keycloakInitOptions, keycloaks } from './keycloak';
import AppRouter from './routes';

import './styles/index.scss';

const queryClient = new QueryClient();

let keycloak = keycloaks[Object.keys(keycloaks)[0]];
const realm = localStorage.getItem('keycloakRealm');
if (realm) {
  keycloak = keycloaks[realm];
}

ReactDOM.render(
  <ReactKeycloakProvider
    authClient={keycloak}
    initOptions={keycloakInitOptions}
    LoadingComponent={<div>Loading</div>}
  >
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  </ReactKeycloakProvider>,
  document.getElementById('root')
);
