import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';

export const Form = () => {
  const { control, handleSubmit } = useForm({
    defaultValues: {
      sin: null,
      first_name: '',
      last_name: '',
      dob: '',
      tax_year: ''
    }
  });

  // We can use react-query.
  const onSubmit = (data) => console.log(data);

  return (
    <form onSubmit={handleSubmit(onSubmit)}>
      <label>SIN</label>
      <Controller
        name="sin"
        control={control}
        render={({ field }) => (
          <TextField type="number" inputProps={{ maxLength: 9 }} {...field} />
        )}
      />
      <label>Surname</label>
      <Controller
        name="last_name"
        control={control}
        render={({ field }) => (
          <TextField inputProps={{ maxLength: 30 }} {...field} />
        )}
      />
      <label>First Name</label>
      <Controller
        name="first_name"
        control={control}
        render={({ field }) => (
          <TextField inputProps={{ maxLength: 30 }} {...field} />
        )}
      />
      <label>Date of Birth</label>
      <Controller
        name="dob"
        control={control}
        render={({ field }) => (
          <TextField
            helperText="yyyymmdd"
            inputProps={{ maxLength: 4 }}
            {...field}
          />
        )}
      />
      <label>Tax Year</label>
      <Controller
        name="tax_year"
        control={control}
        render={({ field }) => (
          <TextField inputProps={{ maxLength: 4 }} {...field} />
        )}
      />
      <Button variant="contained">Submit</Button>
    </form>
  );
};
