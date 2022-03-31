import React, { useEffect } from 'react';
import InputLabel from '@mui/material/InputLabel';
import TextField from '@mui/material/TextField';
import { FormGroup } from '@mui/material';
import { useFormContext } from 'react-hook-form';

const SpouseEmail = ({ name }) => {
  const { setValue, register, unregister } = useFormContext();

  useEffect(() => {
    register(name, { required: true });
    return () => {
      unregister(name);
    };
  }, [register, unregister]);

  return (
    <div>
      <FormGroup>
        <InputLabel htmlFor={name}>Spouse email address:</InputLabel>
        <TextField
          defaultValue=""
          type="text"
          name={name}
          onChange={(e) =>
            setValue(name, e.target.value, { shouldValidate: true })
          }
        />
      </FormGroup>
    </div>
  );
};

export default SpouseEmail;
