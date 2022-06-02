import Box from '@mui/material/Box';
import { useKeycloak } from '@react-keycloak/web';
import React from 'react';
import { BCEID_KEYCLOAK_REALM, BCSC_KEYCLOAK_REALM } from '../config';
import { keycloakInitOptions, keycloaks } from '../keycloak';
const BottomBanner = (props) => {
  const { eligible, text = '', type = '', householdApplicationId = '' } = props;
  const { keycloak } = useKeycloak();
  const redirectUri = householdApplicationId
    ? `${window.location.origin}/householdForm?q=${householdApplicationId}`
    : `${window.location.origin}/form`;
  const buttonText =
    'Please answer the questions above to confirm you are eligible to apply for a rebate.';
  return (
    <>
      <div
        className={
          type === 'individual'
            ? 'start-application-individual'
            : 'start-application-spouse'
        }
      >
        <h1 id="start-text">{text}</h1>
        <Box id="bceid-login-square">
          <h1 id="BceidLoginTitle">BCeID</h1>
          <button
            type="button"
            className="button"
            disabled={
              !eligible ||
              (keycloak.authenticated &&
                keycloak.realm !== BCEID_KEYCLOAK_REALM)
            }
            title={!eligible && buttonText}
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
            Login with BCeID
          </button>
          <button
            type="button"
            className="button"
            disabled={
              !eligible ||
              (keycloak.authenticated && keycloak.realm !== BCSC_KEYCLOAK_REALM)
            }
            title={!eligible && buttonText}
            onClick={() => {
              localStorage.setItem('keycloakRealm', BCSC_KEYCLOAK_REALM);
              if (keycloak.realm === BCSC_KEYCLOAK_REALM) {
                keycloak.login({
                  idpHint: 'bcsc',
                  redirectUri: redirectUri
                });
              } else {
                const bcscKeycloak = keycloaks[BCSC_KEYCLOAK_REALM];
                bcscKeycloak.init(keycloakInitOptions).then(() => {
                  bcscKeycloak.login({
                    idpHint: 'bcsc',
                    redirectUri: redirectUri
                  });
                });
              }
            }}
          >
            Login with BCSC
          </button>
          <div>
            <a
              href="https://www.bceid.ca/register/basic/account_details.aspx?type=regular&eServiceType=basic"
              target="_blank"
              rel="noopener noreferrer"
            >
              Get a Basic BCeID account
            </a>
          </div>
        </Box>
      </div>
    </>
  );
};

export default BottomBanner;
