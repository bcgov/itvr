import React from 'react';
import { useKeycloak } from '@react-keycloak/web';
import EligibilityPageContainer from '../components/Eligibility/EligibilityPageContainer';
import Header from '../components/Header';
function Index() {
  const { keycloak } = useKeycloak();

  return (
    <div className="app">
      <Header />
      <div className="page-content">
        {keycloak.authenticated && (
          <button type="button" onClick={() => keycloak.logout()}>
            Logout
          </button>
        )}
        <EligibilityPageContainer />
      </div>
    </div>
  );
}

export default Index;
