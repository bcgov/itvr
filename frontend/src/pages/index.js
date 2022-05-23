import React from 'react';
import EligibilityPageContainer from '../components/Eligibility/EligibilityPageContainer';
import Layout from '../components/Layout';
import { useDominantKeycloak } from '../keycloak';

function Index() {
  const keycloak = useDominantKeycloak();
  const authenticated = keycloak ? true : false;

  return (
    <div className="app">
      <Layout>
        <EligibilityPageContainer />
      </Layout>
      {authenticated && (
        <button
          type="button"
          onClick={() => {
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
