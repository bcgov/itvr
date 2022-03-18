import Button from '@mui/material/Button';
import React from 'react';

const ApplicationFormPage = (props) => {
  const { handleInputChange, handleSubmit } = props;
  return (
    <div>
      <Button
        onClick={() => {
          handleSubmit();
        }}
        variant="contained"
      >
        Submit
      </Button>
    </div>
  );
};

export default ApplicationFormPage;
