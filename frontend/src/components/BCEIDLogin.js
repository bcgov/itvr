import React from 'react';
import { BCEID_KEYCLOAK_REALM } from '../config';
import { useKeycloak } from '@react-keycloak/web';
import { keycloakInitOptions, keycloaks } from '../keycloak';
const BCEIDLogin = () => {
  const { keycloak } = useKeycloak();
  const redirectUri = `${window.location.origin}/form`;
  return (
    <div>
      <h3>Basic BCeID Account</h3>

      <div>
        <div>Alternate method to confirm your identity.</div>
        <br />
        <div>
          You can also log in with a{' '}
          <a href="https://www.bceid.ca/register/basic/account_details.aspx?type=regular&eServiceType=basic">
            Basic BCeID account
          </a>
          . If you log in with BCeID you will need to upload images of your BC
          Driver’s Licence and a secondary piece of ID.{' '}
          <a href="/identificationExamples">
            Learn more about ID requirements.
          </a>
        </div>
      </div>
      <button
        type="button"
        className="button"
        id="bceid-login-button"
        disabled={
          keycloak.authenticated && keycloak.realm !== BCEID_KEYCLOAK_REALM
        }
        onClick={() => {
          localStorage.setItem('keycloakRealm', BCEID_KEYCLOAK_REALM);
          if (keycloak.realm === BCEID_KEYCLOAK_REALM) {
            keycloak.login({
              idpHint: 'bceid-basic',
              redirectUri: redirectUri
            });
          } else {
            const bceidKeycloak = keycloaks[BCEID_KEYCLOAK_REALM];
            bceidKeycloak.init(keycloakInitOptions).then(() => {
              bceidKeycloak.login({
                idpHint: 'bceid-basic',
                redirectUri: redirectUri
              });
            });
          }
        }}
      >
        Log in with BCeID
      </button>
    </div>
  );
};

export default BCEIDLogin;
