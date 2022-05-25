import { QueryClient, QueryClientProvider } from 'react-query';
import '../src/styles/index.scss';
import { BrowserRouter } from 'react-router-dom';
import { KeycloakProvider, bcscKeycloak, bceidKeycloak } from '../src/keycloak';

export const parameters = {
  actions: { argTypesRegex: '^on[A-Z].*' },
  controls: {
    matchers: {
      color: /(background|color)$/i,
      date: /Date$/
    }
  }
};

const queryClient = new QueryClient();

export const decorators = [
  (Story) => (
    <KeycloakProvider
      authClient={{ bcsc: bcscKeycloak, bceid: bceidKeycloak }}
      initOptions={{
        onLoad: 'check-sso',
        pkceMethod: 'S256'
      }}
      LoadingComponent={<div>Loading</div>}
    >
      <Story />
    </KeycloakProvider>
  ),
  (Story) => (
    <QueryClientProvider client={queryClient}>
      <Story />
    </QueryClientProvider>
  ),
  (Story) => (
    <BrowserRouter>
      <Story />
    </BrowserRouter>
  )
];
