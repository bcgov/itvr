import React from 'react';
import BottomBanner from '../BottomBanner';
import Box from '@mui/material/Box';

const EligibilityPage = (props) => {
  return (
    <Box id="eligibility">
      <div>
        <h2>What you will need to complete this application</h2>
        <h3>Social Insurance Number and CRA income disclosure consent</h3>
        <p>
          Used to confirm your income. To give consent to the Canada Revenue
          Agency (CRA) to disclose your income information.
        </p>
        <h3>BC Driver’s Licence</h3>
        <p>Used to connect you with your rebate. </p>
        <h3>BC Services Card app or Basic BCeID</h3>
        <p>Used to confirm your identity.</p>
        <p>
          The{' '}
          <a href="https://www2.gov.bc.ca/gov/content/governments/government-id/bcservicescardapp">
            BC Services Card app{' '}
          </a>
          is the simplest method to log in and confirm your identity.
        </p>
        <p>
          You can also log in with a{' '}
          <a href="https://www.bceid.ca/register/basic/account_details.aspx?type=regular&eServiceType=basic">
            Basic BCeID account
          </a>
          . If you log in with BCeID you will need to upload images of your BC
          Driver’s Licence and a secondary piece of ID.{' '}
          <a href="/identificationExamples" target="_blank">
            Learn more about ID requirements.
          </a>{' '}
        </p>
        <h3>Household applications</h3>
        <p>
          For a household application your spouse or common law partner will
          also need to confirm their identity and provide CRA income disclosure
          consent, they do not require a driver's licence.{' '}
        </p>
      </div>
      <BottomBanner
        text="Log in to start your rebate application"
        type="individual"
      />
      <h3 id="help-email">I need help</h3>
      <p>
        Contact Go Electric if you have questions about the rebate process or
        your application:
        <ul>
          <li>
            Email{' '}
            <a href="mailto:ZEVPrograms@gov.bc.ca">ZEVPrograms@gov.bc.ca</a>
          </li>
        </ul>
      </p>
    </Box>
  );
};

export default EligibilityPage;
