import React from 'react';
import { FormProvider, useForm, Controller } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useQuery } from 'react-query';
import { useMutation, useQueryClient } from 'react-query';
import FormGroup from '@mui/material/FormGroup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import ConsentPersonal from './ConsentPersonal';
import ConsentTax from './ConsentTax';
import FileDropArea from './upload/FileDropArea';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';

export const defaultValues = {
  application: '',
  sin: '',
  first_name: '',
  last_name: '',
  middle_names: '',
  email: '',
  address: '',
  city: '',
  postal_code: '',
  date_of_birth: '',
  documents: [],
  consent_personal: false,
  consent_tax: false
};

const SpouseForm = ({ id }) => {
  const queryClient = useQueryClient();
  const methods = useForm({
    defaultValues
  });
  const applicationId = id;
  const { control, handleSubmit, register, watch } = methods;
  const axiosInstance = useAxios();

  const queryFn = () =>
    axiosInstance.current
      .get(`/api/spouse-application/${id}/initiate`)
      .then((response) => response.data);

  const { data, isLoading, isError, error } = useQuery(
    ['application', id],
    queryFn
  );

  const navigate = useNavigate();
  const mutation = useMutation((data) => {
    const formData = new FormData();
    data['application'] = id;
    for (const [key, value] of Object.entries(data)) {
      if (key === 'documents') {
        formData.append('doc1', value[0]);
        formData.append('doc2', value[1]);
      } else {
        formData.append(key, value);
      }
    }
    return axiosInstance.current.post('/api/spouse-application', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  });
  const onSubmit = (data) =>
    mutation.mutate(data, {
      onSuccess: (data, variables, context) => {
        queryClient.setQueryData(['application', applicationId], data.data);
        navigate(`/details/${applicationId}/household`);
      }
    });

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (isError) {
    return <p>{error.message}</p>;
  }
  const { address, city, postal_code: postalCode } = data;
  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit)}>
        <span>
          <InputLabel htmlFor="address">Street Address:</InputLabel>
          <p>{address}</p>
        </span>
        <span>
          <InputLabel htmlFor="city">City:</InputLabel>
          <p>{city}</p>
        </span>
        <span>
          <InputLabel htmlFor="postal_code">Postal Code:</InputLabel>
          <p>{postalCode}</p>
        </span>
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
          <Box mt={2}>
            <InputLabel htmlFor="documents">
              Upload an image (jpg or png) of your B.C. Driver's Licence or B.C.
              Services Card (photo side) and a secondary piece of ID (see
              examples):
            </InputLabel>
          </Box>
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

export default SpouseForm;
