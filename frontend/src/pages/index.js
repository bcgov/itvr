import React from 'react';
import { useKeycloak } from '@react-keycloak/web';

function Index() {
  const { keycloak } = useKeycloak();

  return (
    <div>
      {keycloak.authenticated && (
        <button type="button" onClick={() => keycloak.logout()}>
          Logout
        </button>
      )}

      <button type="button" onClick={() => keycloak.login({ idpHint: 'bceid-basic', redirectUri: `${window.location.origin}/form` })}>
        BCeID
      </button>

      <button type="button" onClick={() => keycloak.login({ idpHint: 'idir', redirectUri: `${window.location.origin}/admin` })}>
        IDIR
      </button>
    </div>
  );
};

export default Index;
