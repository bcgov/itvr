import Box from '@mui/material/Box';
import React from 'react';
import { useKeycloak } from '@react-keycloak/web';
const BottomBanner = (props) => {
  const { eligible, taxYear } = props;
  const { keycloak } = useKeycloak();
  return (
    <>
      <div id="start-application">
        <h1 id="start-text">Start your rebate application</h1>
        <Box id="bceid-login-square">
          <h1>BCeID</h1>
          <button
            type="button"
            className="button"
            disabled={!eligible}
            onClick={() =>
              keycloak.login({
                idpHint: 'bceid-basic',
                redirectUri: `${window.location.origin}/form`
              })
            }
          >
            Login with BCeID
          </button>
          <div>
            <a href="https://www.bceid.ca/register/basic/account_details.aspx?type=regular&eServiceType=basic">
              Get a Basic BCeID account
            </a>
          </div>
        </Box>
        * UP Until June 30 your ${taxYear} notice of assessment (NOA) will be
        used to determine your rebate amount. On July 1 it will change to use
        your {taxYear} NOA.
      </div>
    </>
  );
};

export default BottomBanner;
