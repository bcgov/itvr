import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import React, { useState } from 'react';
import TextField from '@mui/material/TextField';

const ApplicationFormPage = (props) => {
  const {
     handleInputChange, handleSubmit,
  } = props;
  return (
    <div>
      <Box
        component="form"
        sx={{
          '& .MuiTextField-root': { my: 1, width: '25ch' },
        }}
        noValidate
        autoComplete="off"
      >
        <div>
          <TextField
            required
            name="sin"
            id="sin"
            label="Social Insurance Number"
            onInput={(event) => { handleInputChange(event); }}
          />
        </div>
        <div>
          <TextField
            required
            name="last_name"
            id="outlined-helperText"
            label="Surname"
            inputProps={
              { maxLength: 30 }
              }
            onInput={(event) => { handleInputChange(event); }}
          />
        </div>
        <div>
          <TextField
            required
            name="first_name"
            id="outlined-helperText"
            label="First Name"
            inputProps={
                { maxLength: 30 }
                }
            onInput={(event) => { handleInputChange(event); }}
          />
        </div>
        <div>
          <TextField
            required
            name="dob"
            id="outlined-helperText"
            label="Date of Birth"
            helperText="yyyymmdd"
            inputProps={
                { maxLength: 8 }
                }
            onInput={(event) => { handleInputChange(event); }}
          />
        </div>
        <div>
          <TextField
            required
            name="tax_year"
            id="outlined-helperText"
            label="Tax Year"
            helperText=""
            inputProps={
                { maxLength: 4 }
                }
            onInput={(event) => { handleInputChange(event); }}
          />
        </div>
        <Button
          onClick={() => {
            handleSubmit();
          }}
          variant="contained"
        >
          Submit
        </Button>
      </Box>
    </div>
  );
};

export default ApplicationFormPage;
