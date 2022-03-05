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

      <button type="button" onClick={() => keycloak.login({ idpHint: 'bceid-basic', redirectUri: 'http://localhost:3000/form' })}>
        BCeID
      </button>

      <button type="button" onClick={() => keycloak.login({ idpHint: 'idir', redirectUri: 'http://localhost:3000/admin' })}>
        IDIR
      </button>
    </div>
  );
};

export default Index;
