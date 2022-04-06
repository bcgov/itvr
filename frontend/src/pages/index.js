import React from 'react';
import { useKeycloak } from '@react-keycloak/web';
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
        <button type="button" onClick={() => keycloak.logout()}>
          Logout
        </button>
      )}
    </div>
  );
}

export default Index;
