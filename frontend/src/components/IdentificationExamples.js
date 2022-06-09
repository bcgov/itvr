import React from 'react';
import Box from '@mui/material/Box';
import dl from '../styles/images/sample-dl.png';
import bceid from '../styles/images/sample-bcsc.png';
import bankStatement from '../styles/images/sample-bank-statement.png';
import utility from '../styles/images/sample-utility-statement.png';

const IdentificationExamples = (props) => {
  return (
    <Box className="identification">
      <h2>Identification requirements for rebate applications using BCeID</h2>
      <h3>Names and addresses must be the same</h3>
      <ul>
        <li>Both pieces of your ID must show the same name and address.</li>
        <li>
          Both pieces of ID from both members of a household must have the same
          address.
        </li>
      </ul>
      <h3>Primary identification</h3>
      <p>A passport cannot be used as ID as it doesn't show your address.</p>
      <h4>BC Driver's Licence</h4>
      <ul>
        <li>An image of the primary applicant's BC Driver's Licence.</li>
      </ul>

      <Box
        className="left-img"
        component="img"
        sx={{
          maxWidth: 400
        }}
        alt="A photograph of the front of the spouse's BC Service Card clearly showing the photograph and address"
        src={dl}
      />
      <h4>BC Services Card</h4>
      <ul>
        <li>
          The spouse of a household application can use a BC Services Card or
          driver's licence.
        </li>
      </ul>
      <Box
        component="img"
        sx={{
          maxWidth: 400
        }}
        alt="A photograph of the front of the applicant's BC Driver’s Licence clearly showing the photograph and address"
        src={bceid}
      />

      <h3>Secondary Identification</h3>
      <p>
        The secondary piece of identification gives further proof of your name
        and address.
      </p>
      <h4>Accepted secondary identification</h4>
      <p>Your secondary ID must show the same address as your primary ID.</p>
      <h5>BC Services Card</h5>
      <ul>
        <li>
          A BC Services Card can be used if your primary ID is your driver's
          licence.
        </li>
      </ul>
      <h5>Financial statements and utility bills</h5>
      <ul>
        <li>Must have been issued in the last 90 days.</li>
        <li>Only show the letterhead, date, name and address. </li>
        <li>
          To protect your personal information, obscure or do not display your
          account details.
        </li>
      </ul>

      <Box
        className="left-img"
        component="img"
        mb={3}
        sx={{
          maxWidth: 400,
          display: 'block'
        }}
        src={bankStatement}
        alt="A photograph of a portion of a bank statement showing the company letterhead, applicant's name, address and the date the statement was issued. Personal information like account details are not displayed or blocked out by felt pen."
      />
      <Box
        component="img"
        sx={{
          maxWidth: 500,
          maxHeight: '60%'
        }}
        alt="A photograph of a portion of a utility statement showing the company letterhead, applicant's name, address and the date the statement was issued. Personal information like account details are not displayed or blocked out by felt pen."
        src={utility}
      />
    </Box>
  );
};
export default IdentificationExamples;
