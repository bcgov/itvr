import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import axios from 'axios';
import React, { useEffect, useRef, useState } from 'react';
import TextField from '@mui/material/TextField';

const ApplicationFormPage = (props) => {
  const {
    loading, handleInputChange, details, handleSubmit,
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
            name="SIN"
            id="SIN"
            label="Social Insurance Number"
            onInput={(event) => { handleInputChange(event); }}
          />
        </div>
        <div>
          <TextField
            required
            name="surname"
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
            name="firstname"
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
            name="taxyear"
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
            console.log('click')
            // handleSubmit();
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
