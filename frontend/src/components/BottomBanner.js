import Box from '@mui/material/Box';
import { useKeycloak } from '@react-keycloak/web';
import React from 'react';
import { BCEID_KEYCLOAK_REALM, BCSC_KEYCLOAK_REALM } from '../config';
import { keycloakInitOptions, keycloaks } from '../keycloak';
const BottomBanner = (props) => {
  const { text = '', type = '', householdApplicationId = '' } = props;
  const { keycloak } = useKeycloak();
  const redirectUri = householdApplicationId
    ? `${window.location.origin}/householdForm?q=${householdApplicationId}`
    : `${window.location.origin}/form`;

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
        <Box sx={{ flexWrap: 'wrap', flexDirection: 'row' }}>
          <Box className="login-square">
            <h2>BC Services Card app</h2>
            <button
              type="button"
              className="button"
              disabled={
                keycloak.authenticated && keycloak.realm !== BCSC_KEYCLOAK_REALM
              }
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
              Log in with BC Services Card
            </button>
            <div>
              <a href="https://www2.gov.bc.ca/gov/content/governments/government-id/bcservicescardapp">
                Get the BC Services Card app
              </a>
            </div>
          </Box>
        </Box>
      </div>
    </>
  );
};

export default BottomBanner;
