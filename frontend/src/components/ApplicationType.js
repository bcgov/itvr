import React, { useState, useEffect } from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Box from '@mui/material/Box';
import Typography from '@mui/material/Typography';
import InputLabel from '@mui/material/InputLabel';
import { Controller } from 'react-hook-form';
import TextField from '@mui/material/TextField';
import { FormGroup } from '@mui/material';
import { useFormContext } from 'react-hook-form';

// we want to save the radio selection for if its individual or household, and if its household also save the spouse email address
//if submitted with individual type, CLEAR spouse email
const SpouseEmail = ({ control, applicationType }) => {
  return (
    <FormGroup>
      <InputLabel htmlFor="spouse_email">Spouse email address:</InputLabel>
      <Controller
        name="spouse_email"
        control={control}
        render={({ field }) => (
          <TextField
            disabled={applicationType === 'individual'}
            id="spouse_email"
            inputProps={{ maxLength: 250 }}
            {...field}
          />
        )}
      />
    </FormGroup>
  );
};

const ApplicationType = ({ control }) => {
  const [applicationType, setApplicationType] = useState(false);
  return (
    <Box my={5}>
      <FormControl>
        <FormLabel className="label" id="application-type" sx={{ mb: 1 }}>
          If you can receive a larger rebate applying as a household your spouse
          or common law partner will need to complete a portion of this
          application to confirm their identity and provide their CRA income
          disclosure consent. Instructions will be sent to them by email.
        </FormLabel>
        <RadioGroup
          aria-labelledby="application-type"
          name="application-type"
          onChange={(e) => setApplicationType(e.target.value)}
        >
          <FormControlLabel
            value="individual"
            control={<Radio />}
            label={
              <Typography color="textPrimary" fontWeight="bold">
                {'Apply as an individual'}
              </Typography>
            }
          />
          <FormControlLabel
            value="household"
            control={<Radio />}
            label={
              <Typography color="textPrimary">
                {
                  <>
                    {' '}
                    <b>Apply as a household,</b> enter your spouse or common law
                    partner's email address below.
                  </>
                }
              </Typography>
            }
          />
        </RadioGroup>
      </FormControl>

      <SpouseEmail applicationType={applicationType} />

      <Box mt={2}>
        <sup>3</sup>
        <sub>
          <b>Household:</b> a person or group of persons who occupy the same
          dwelling and do not have a usual place of residence elsewhere in
          Canada or abroad. The dwelling may be either a collective dwelling or
          a private dwelling.
        </sub>
      </Box>
      <Box mt={2}>
        <sup>4</sup>
        <sub>
          <b>Spouse:</b> someone of the same or opposite gender who has one of
          the following types of relationship to you (1) they are married to you
          (2) they are living in a marriage-like relationship with you.
        </sub>
      </Box>
    </Box>
  );
};
export default ApplicationType;
