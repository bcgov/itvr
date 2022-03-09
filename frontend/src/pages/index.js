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
      <button
        type="button"
        onClick={() =>
          keycloak.login({
            idpHint: 'idir',
            redirectUri: `${window.location.origin}/admin`
          })
        }
      >
        IDIR
      </button>
    </div>
  );
}

export default Index;
