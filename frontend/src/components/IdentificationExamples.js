import React from 'react';
import Box from '@mui/material/Box';
import dl from '../styles/images/sample-dl.png';
import bceid from '../styles/images/sample-bcsc.png';
import bankStatement from '../styles/images/sample-bank-statement.png';
import utility from '../styles/images/samle-utility-statement.png';
import Button from '@mui/material/Button';

const IdentificationExamples = (props) => {
  return (
    <Box className="identification">
      <h3>Identification Requirements for Basic BCeID Rebate Applications</h3>
      <p>
        A photo of the applicant's B.C. Driver's Licence (the spouse of a
        household aplication can use a B.C. Services Card) and 1 piece of
        secondary ID as shown below are required for rebate applications made
        using Basic BCeID.
      </p>
      <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
        <Box
          className="left-img"
          component="img"
          sx={{
            maxWidth: 400
          }}
          alt="example driver's license"
          src={dl}
        />
        <Box
          component="img"
          sx={{
            maxWidth: 400
          }}
          alt="example of BCEID"
          src={bceid}
        />
      </Box>
      <h3>Secondary Identification</h3>
      <p>
        The secondary piece of identification is intended to provide proof of
        address when using Basic BCeID. For example a financial statement or
        utility bill. It must have been issued within the last 90 days and the
        name and address must match that on the applicants driver’s licence.
        Only the letterhead, date, name and address portion should be shown,
        account details should be obscured or not displayed.
      </p>
      <Box sx={{ display: 'flex', flexWrap: 'wrap' }}>
        <Box
          className="left-img"
          component="img"
          sx={{
            maxWidth: 400
          }}
          src={bankStatement}
          alt="example bank statement with account number covered and only the header and applicant's address visible"
        />
        <Box
          component="img"
          sx={{
            maxWidth: 500,
            maxHeight: '60%'
          }}
          alt="example of utility bill with account number covered and only the header and applicant's address visible"
          src={utility}
        />
      </Box>
      <Button sx={{ mt: 5 }} variant="contained" onClick={() => window.close()}>
        Close
      </Button>
    </Box>
  );
};
export default IdentificationExamples;
