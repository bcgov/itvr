/* eslint-disable react/jsx-indent */
import React from 'react';
import Checkbox from '@mui/material/Checkbox';
import FormGroup from '@mui/material/FormGroup';
import FormControlLabel from '@mui/material/FormControlLabel';

const ApplicationConsent = (props) => {
  const { title } = props;
  const label =
    'I understand that by submitting this application form it means:';
  return (
    <div>
      <h3>{title}</h3>
      <p>
        You must read the following statements and use the checkbox to indicate
        that you understand and agree.
      </p>
      <FormGroup>
        <FormControlLabel control={<Checkbox />} label={label} />
      </FormGroup>
    </div>
  );
};

export default ApplicationConsent;
