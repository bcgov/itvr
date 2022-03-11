import React from 'react';
import { useKeycloak } from '@react-keycloak/web';
import EligibilityPageContainer from '../components/Eligibility/EligibilityPageContainer';

function Index() {
  const { keycloak } = useKeycloak();

  return (
    <div>
      {keycloak.authenticated && (
        <button type="button" onClick={() => keycloak.logout()}>
          Logout
        </button>
      )}
      <EligibilityPageContainer />
    </div>
  );
}

export default Index;
