import Box from '@mui/material/Box';
import React from 'react';
import { useKeycloak } from '@react-keycloak/web';
const BottomBanner = (props) => {
  const { eligible, text = '', type = '' } = props;
  const { keycloak } = useKeycloak();
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
