import { useKeycloak } from '@react-keycloak/web';
import React from 'react';
import EligibilityPageContainer from '../components/Eligibility/EligibilityPageContainer';
import Layout from '../components/Layout';

function Index() {
  const { keycloak } = useKeycloak();

  return (
    <div className="app">
      <Layout>
        <EligibilityPageContainer />
      </Layout>
      {keycloak.authenticated && (
        <button
          type="button"
          onClick={() => {
            localStorage.removeItem('keycloakRealm');
            keycloak.logout();
          }}
        >
          Logout
        </button>
      )}
    </div>
  );
}

export default Index;
