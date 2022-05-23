import Box from '@mui/material/Box';
import React from 'react';
import { useKeycloaks } from '../keycloak';
const BottomBanner = (props) => {
  const { eligible, text = '', type = '', householdApplicationId = '' } = props;
  const keycloaks = useKeycloaks();
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
            disabled={!eligible /*|| keycloaks.bcsc.authenticated*/}
            title={!eligible && buttonText}
            onClick={() =>
              keycloaks.bceid.login({
                idpHint: 'bceid-basic',
                redirectUri: redirectUri
              })
            }
          >
            Login with BCeID
          </button>
          <button
            type="button"
            className="button"
            disabled={!eligible /*|| keycloaks.bceid.authenticated*/}
            title={!eligible && buttonText}
            onClick={() => {
              keycloaks.bcsc.login({
                idpHint: 'bcsc',
                redirectUri: redirectUri
              });
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
