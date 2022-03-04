import * as React from 'react';
import { useKeycloak } from '@react-keycloak/web';

export default () => {
  const { keycloak } = useKeycloak();

  return (
    <div>
      {keycloak.authenticated && (
        <button type="button" onClick={() => keycloak.logout()}>
          Logout
        </button>
      )}

      <button type="button" onClick={() => keycloak.login({ idpHint: 'bceid-basic' })}>
        BCeID
      </button>

      <button type="button" onClick={() => keycloak.login({ idpHint: 'idir' })}>
        IDIR
      </button>
    </div>
  );
};
