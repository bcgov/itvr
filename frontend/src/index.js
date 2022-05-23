import React from 'react';
import ReactDOM from 'react-dom';
import { QueryClient, QueryClientProvider } from 'react-query';
import AppRouter from './routes';
import { KeycloakContext, keycloaks } from './keycloak';
import './styles/index.scss';

const queryClient = new QueryClient();

const initOptions = {
  onLoad: 'check-sso',
  pkceMethod: 'S256'
};

const keycloakPromises = [];
for (const i in keycloaks) {
  keycloakPromises.push(keycloaks[i].init(initOptions));
}

Promise.all(keycloakPromises).then((values) => {
  ReactDOM.render(
    <KeycloakContext.Provider value={keycloaks}>
      <QueryClientProvider client={queryClient}>
        <AppRouter />
      </QueryClientProvider>
    </KeycloakContext.Provider>,
    document.getElementById('root')
  );
});
