import { ReactKeycloakProvider } from '@react-keycloak/web';
import { QueryClient, QueryClientProvider } from 'react-query';
import keycloak from '../src/keycloak';
import '../src/styles/index.scss';

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
    <ReactKeycloakProvider authClient={keycloak}>
      <Story />
    </ReactKeycloakProvider>
  ),
  (Story) => (
    <QueryClientProvider client={queryClient}>
      <Story />
    </QueryClientProvider>
  )
];
