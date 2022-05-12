import React from 'react';
import EligibilityPageContainer from '../components/Eligibility/EligibilityPageContainer';
import Layout from '../components/Layout';
import useCustomKeycloak from '../utils/keycloakHook';

function Index() {
  const { keycloak } = useCustomKeycloak();

  return (
    <div className="app">
      <Layout>
        <EligibilityPageContainer />
      </Layout>
      {keycloak.authenticated && (
        <button type="button" onClick={() => keycloak.logout()}>
          Logout
        </button>
      )}
    </div>
  );
}

export default Index;
