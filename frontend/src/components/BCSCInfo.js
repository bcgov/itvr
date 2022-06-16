import React from 'react';
import Box from '@mui/material/Box';

const BCSCInfo = ({ kcToken }) => {
  return (
    <>
      <p>
        Your name, date of birth and address below has been provided from your
        BC Services Card app.
      </p>
      <Box sx={{ maxWidth: '550px' }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>Your last name (surname):</span>
          <span className="primary-answer">{kcToken.family_name}</span>
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>First name (given name):</span>
          <span className="primary-answer">{kcToken.given_name}</span>
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>Date of birth:</span>
          <span className="primary-answer">{kcToken.birthdate}</span>
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>Street address:</span>
          <span className="primary-answer">{kcToken.street_address}</span>
        </Box>
        <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
          <span>City:</span>
          <span className="primary-answer">{kcToken.locality}</span>
        </Box>
        {kcToken.postal_code && (
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Postal code:</span>
            <span className="primary-answer">{kcToken.postal_code}</span>
          </Box>
        )}
      </Box>
    </>
  );
};
export default BCSCInfo;
