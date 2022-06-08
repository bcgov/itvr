import React from 'react';
import ReactDOM from 'react-dom';
import { ReactKeycloakProvider } from '@react-keycloak/web';
import { QueryClient, QueryClientProvider } from 'react-query';
import { getKeycloak, keycloakInitOptions } from './keycloak';
import AppRouter from './routes';
import Footer from './components/Footer';

import './styles/index.scss';
import Loading from './components/Loading';

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
      <Footer />
    </QueryClientProvider>
  </ReactKeycloakProvider>,
  document.getElementById('root')
);
