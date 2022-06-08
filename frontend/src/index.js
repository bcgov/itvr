import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import { QueryClient, QueryClientProvider } from 'react-query';
import { getKeycloak, keycloakInitOptions } from './keycloak';
import AppRouter from './routes';
import Loading from './components/Loading';
import './styles/index.scss';

const queryClient = new QueryClient();
const keycloak = getKeycloak();

ReactDOM.render(
  <ReactKeycloakProvider
    authClient={keycloak}
    initOptions={keycloakInitOptions}
    LoadingComponent={<Loading open={true} />}
  >
    <QueryClientProvider client={queryClient}>
      <AppRouter />
    </QueryClientProvider>
  </ReactKeycloakProvider>,
  document.getElementById('root')
);
