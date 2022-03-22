import React from 'react';
import { FormProvider, useForm, Controller } from 'react-hook-form';
import FormGroup from '@mui/material/FormGroup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import ConsentPersonal from './ConsentPersonal';
import ConsentTax from './ConsentTax';
import FileDropArea from './upload/FileDropArea';

export const defaultValues = {
  sin: '',
  first_name: '',
  last_name: '',
  dob: '',
  tax_year: '',
  documents: []
};

const Form = () => {
  const methods = useForm({
    defaultValues
  });

  const { control, handleSubmit } = methods;

  // We can use react-query.
  const onSubmit = (data) => console.log(data);

  return (
    <FormProvider {...methods}>
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
              <TextField
                id="tax_year"
                inputProps={{ maxLength: 4 }}
                {...field}
              />
            )}
          />
          <FormGroup>
            <FileDropArea />
          </FormGroup>
          <FormGroup>
            <ConsentPersonal />
          </FormGroup>
          <FormGroup>
            <ConsentTax />
          </FormGroup>
          <Button variant="contained" type="submit">
            Submit
          </Button>
        </FormGroup>
      </form>
    </FormProvider>
  );
};

export default Form;
