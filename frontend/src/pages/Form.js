import * as React from 'react';
import { useKeycloak } from '@react-keycloak/web';

export default () => {
  const { keycloak } = useKeycloak();

  return (
    <div>
      Hello BCeID
    </div>
  );
};
