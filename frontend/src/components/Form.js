import React from 'react';
import { FormProvider, useForm, Controller } from 'react-hook-form';
import { useMutation } from 'react-query';
import FormGroup from '@mui/material/FormGroup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import ConsentPersonal from './ConsentPersonal';
import ConsentTax from './ConsentTax';
import FileDropArea from './upload/FileDropArea';
import useAxios from '../utils/axiosHook';

export const defaultValues = {
  sin: '',
  first_name: '',
  last_name: '',
  middle_names: '',
  email: '',
  address: '',
  city: '',
  postal_code: '',
  dob: '',
  drivers_licence: '',
  documents: [],
  consent_personal: false,
  consent_tax: false
};

const Form = () => {
  const methods = useForm({
    defaultValues
  });
  const { control, handleSubmit } = methods;
  const axiosInstance = useAxios();
  const mutation = useMutation((data) => {
    console.log(data);
    const formData = new FormData();
    for (const [key, value] of Object.entries(data)) {
      if (key === 'documents') {
        formData.append('doc1', value[0]);
        formData.append('doc2', value[1]);
      } else {
        formData.append(key, value);
      }
    }
    formData.append('tax_year', 2021);
    return axiosInstance.current.post('/api/application-form', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  });
  const onSubmit = (data) => mutation.mutate(data);

  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <FormGroup>
          <InputLabel htmlFor="last_name">Last Name (Surname):</InputLabel>
          <Controller
            name="last_name"
            control={control}
            render={({ field }) => (
              <TextField
                id="last_name"
                inputProps={{ maxLength: 250 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="first_name">First Name (Given Name):</InputLabel>
          <Controller
            name="first_name"
            control={control}
            render={({ field }) => (
              <TextField
                id="first_name"
                inputProps={{ maxLength: 250 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="middle_names">Middle Names(s):</InputLabel>
          <Controller
            name="middle_names"
            control={control}
            render={({ field }) => (
              <TextField
                id="middle_names"
                inputProps={{ maxLength: 250 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="email">Email Address:</InputLabel>
          <Controller
            name="email"
            type="email"
            control={control}
            render={({ field }) => (
              <TextField
                id="email"
                inputProps={{ maxLength: 250 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="date_of_birth">Date of Birth:</InputLabel>
          <Controller
            name="date_of_birth"
            control={control}
            render={({ field }) => (
              <TextField id="date_of_birth" type="date" {...field} />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="address">Street Address:</InputLabel>
          <Controller
            name="address"
            control={control}
            render={({ field }) => (
              <TextField
                id="address"
                inputProps={{ maxLength: 250 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="city">City:</InputLabel>
          <Controller
            name="city"
            control={control}
            render={({ field }) => (
              <TextField id="city" inputProps={{ maxLength: 250 }} {...field} />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="postal_code">Postal Code:</InputLabel>
          <Controller
            name="postal_code"
            control={control}
            render={({ field }) => (
              <TextField
                id="postal_code"
                inputProps={{ maxLength: 6 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="sin">Social Insurance Number (SIN):</InputLabel>
          <Controller
            name="sin"
            control={control}
            render={({ field }) => (
              <TextField id="sin" inputProps={{ maxLength: 9 }} {...field} />
            )}
          />
        </FormGroup>
        <FormGroup>
          <InputLabel htmlFor="drivers_licence">
            B.C. Driver's Licence Number:
          </InputLabel>
          <Controller
            name="drivers_licence"
            control={control}
            render={({ field }) => (
              <TextField
                id="drivers_licence"
                inputProps={{ maxLength: 9 }}
                {...field}
              />
            )}
          />
        </FormGroup>
        <FormGroup>
          <FileDropArea name="documents" />
        </FormGroup>
        <FormGroup>
          <ConsentPersonal name="consent_personal" />
        </FormGroup>
        <FormGroup>
          <ConsentTax name="consent_tax" />
        </FormGroup>
        <Button variant="contained" type="submit">
          Submit
        </Button>
      </form>
    </FormProvider>
  );
};

export default Form;
