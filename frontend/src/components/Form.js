import React from 'react';
import { useForm, Controller } from 'react-hook-form';
import FormGroup from '@mui/material/FormGroup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';

const Form = () => {
  const { control, handleSubmit } = useForm({
    defaultValues: {
      sin: '',
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
      <FormGroup>
        <InputLabel htmlFor="sin">SIN</InputLabel>
        <Controller
          name="sin"
          control={control}
          render={({ field }) => (
            <TextField id="sin" inputProps={{ maxLength: 9 }} {...field} />
          )}
        />
      </FormGroup>
      <FormGroup>
        <InputLabel htmlFor="last_name">Surname</InputLabel>
        <Controller
          name="last_name"
          control={control}
          render={({ field }) => (
            <TextField
              id="last_name"
              inputProps={{ maxLength: 30 }}
              {...field}
            />
          )}
        />
      </FormGroup>
      <FormGroup>
        <InputLabel htmlFor="first_name">First Name</InputLabel>
        <Controller
          name="first_name"
          control={control}
          render={({ field }) => (
            <TextField
              id="first_name"
              inputProps={{ maxLength: 30 }}
              {...field}
            />
          )}
        />
      </FormGroup>
      <FormGroup>
        <InputLabel htmlFor="dob">Date of Birth</InputLabel>
        <Controller
          name="dob"
          control={control}
          render={({ field }) => (
            <TextField id="dob" inputProps={{ maxLength: 4 }} {...field} />
          )}
        />
      </FormGroup>
      <FormGroup>
        <InputLabel htmlFor="tax_year">Tax Year</InputLabel>
        <Controller
          name="tax_year"
          control={control}
          render={({ field }) => (
            <TextField id="tax_year" inputProps={{ maxLength: 4 }} {...field} />
          )}
        />
        <Button variant="contained" type="submit">
          Submit
        </Button>
      </FormGroup>
    </form>
  );
};

export default Form;
