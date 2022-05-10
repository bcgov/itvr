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
import { isAgeValid, isSINValid } from '../utility';

export const defaultValues = {
  application: '',
  sin: '',
  first_name: '',
  last_name: '',
  middle_names: '',
  address: '',
  city: '',
  postal_code: '',
  date_of_birth: '',
  documents: [],
  consent_personal: false,
  consent_tax: false
};

const SpouseForm = ({ id, setNumberOfErrors, setErrorsExistCounter }) => {
  const queryClient = useQueryClient();
  const methods = useForm({
    defaultValues
  });
  const applicationId = id;
  const {
    control,
    handleSubmit,
    register,
    watch,
    formState: { errors },
    setValue
  } = methods;
  const axiosInstance = useAxios();

  const queryFn = () =>
    axiosInstance.current
      .get(`/api/application-form/${id}/household`)
      .then((response) => response.data);

  const { data, isLoading, isError, error } = useQuery(
    ['spouse-application', id],
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
  const onSubmit = (data) => {
    setNumberOfErrors(0);
    mutation.mutate(data, {
      onSuccess: (data, variables, context) => {
        queryClient.setQueryData(
          ['spouse-application', applicationId],
          data.data
        );
        navigate(`/details/${applicationId}/household`);
      }
    });
  };

  const onError = (errors) => {
    const numberOfErrors = Object.keys(errors).length;
    setNumberOfErrors(numberOfErrors);
    if (numberOfErrors > 0) {
      setErrorsExistCounter((prev) => {
        return prev + 1;
      });
    }
  };

  if (isLoading) {
    return <p>Loading...</p>;
  }
  if (isError) {
    return <p>{error.message}</p>;
  }
  const { address, city, postal_code: postalCode } = data;
  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit, onError)}>
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
          {errors?.last_name?.type === 'required' && (
            <p className="error">Last Name cannot be blank</p>
          )}
          <InputLabel htmlFor="last_name">Last Name (Surname):</InputLabel>
          <Controller
            name="last_name"
            control={control}
            render={({ field }) => (
              <TextField
                id="last_name"
                inputProps={{ maxLength: 250 }}
                onChange={(e) => setValue('last_name', e.target.value)}
              />
            )}
            rules={{ required: true }}
          />
        </FormGroup>
        <FormGroup>
          {errors?.first_name?.type === 'required' && (
            <p className="error">First Name cannot be blank</p>
          )}
          <InputLabel htmlFor="first_name">First Name (Given Name):</InputLabel>
          <Controller
            name="first_name"
            control={control}
            render={({ field }) => (
              <TextField
                id="first_name"
                inputProps={{ maxLength: 250 }}
                onChange={(e) => setValue('first_name', e.target.value)}
              />
            )}
            rules={{ required: true }}
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
          {errors?.date_of_birth?.type === 'validate' && (
            <p className="error">
              You must be 16 years or older to request a rebate, please check
              the date of birth entered.
            </p>
          )}
          <InputLabel htmlFor="date_of_birth">Date of Birth:</InputLabel>
          <Controller
            name="date_of_birth"
            control={control}
            render={({ field }) => (
              <TextField
                id="date_of_birth"
                type="date"
                onChange={(e) => setValue('date_of_birth', e.target.value)}
              />
            )}
            rules={{
              validate: (inputtedDOB) => {
                return isAgeValid(inputtedDOB, 16);
              }
            }}
          />
        </FormGroup>
        <FormGroup>
          {errors?.sin?.type === 'validate' && (
            <p className="error">Not a valid SIN</p>
          )}
          <InputLabel htmlFor="sin">Social Insurance Number (SIN):</InputLabel>
          <Controller
            name="sin"
            control={control}
            render={({ field }) => (
              <TextField
                id="sin"
                inputProps={{ maxLength: 9 }}
                onChange={(e) => setValue('sin', e.target.value)}
              />
            )}
            rules={{
              validate: (inputtedSIN) => {
                return isSINValid(inputtedSIN);
              }
            }}
          />
        </FormGroup>
        <FormGroup>
          <Box mt={2}>
            <InputLabel htmlFor="documents">
              Upload an image (jpg or png) of your B.C. Driver's Licence or B.C.
              Services Card (photo side) and a secondary piece of ID &nbsp;
              <a href="/identificationExamples" target="_blank">
                (see examples):
              </a>
            </InputLabel>
          </Box>
          {errors?.documents?.type === 'validate' && (
            <p className="error">Need at least 2 files</p>
          )}
          {errors?.documents?.type === 'maxSize' && (
            <p className="error">No file may exceed 5MB</p>
          )}
          <FileDropArea name="documents" />
        </FormGroup>
        <FormGroup>
          <ConsentPersonal name="consent_personal" required={true} />
        </FormGroup>
        <FormGroup>
          <ConsentTax name="consent_tax" required={true} />
        </FormGroup>
        <Button variant="contained" type="submit">
          Submit
        </Button>
      </form>
    </FormProvider>
  );
};

export default SpouseForm;
