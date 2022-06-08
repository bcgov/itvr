import React, { useState } from 'react';
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
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import { isAgeValid, isSINValid } from '../utility';
import LockIcon from '@mui/icons-material/Lock';
import Upload from './upload/Upload';
import Loading from './Loading';

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
  const [loading, setLoading] = useState(false);
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
    setLoading(true);
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
      <Loading open={loading} />
      <form onSubmit={handleSubmit(onSubmit, onError)}>
        <h2>Apply for a passenger vehicle rebate</h2>
        <Box sx={{ display: 'inline' }}>
          <h3 id="form-submission-title">
            Complete your household rebate application <LockIcon />
          </h3>
          <span> secure form submission</span>
        </Box>
        <p>
          The address information below has been provided from your household
          application and must match your identification.
        </p>
        <Box sx={{ maxWidth: '550px' }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>Street address:</span>
            <span className="primary-answer">{address}</span>
          </Box>
          <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
            <span>City:</span>
            <span className="primary-answer">{city}</span>
          </Box>
          {postalCode && (
            <Box sx={{ display: 'flex', justifyContent: 'space-between' }}>
              <span>Postal code:</span>
              <span className="primary-answer">{postalCode}</span>
            </Box>
          )}
        </Box>
        <FormGroup>
          {errors?.last_name?.type === 'required' && (
            <p className="error">Last Name cannot be blank</p>
          )}
          <InputLabel sx={{ color: 'black' }} htmlFor="last_name">
            Your last name (surname):
          </InputLabel>
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
          <InputLabel htmlFor="first_name" sx={{ color: 'black' }}>
            First name (given name):
          </InputLabel>
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
          <InputLabel htmlFor="middle_names" sx={{ color: 'black' }}>
            Middle names(s) (optional):
          </InputLabel>
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
          <InputLabel htmlFor="date_of_birth" sx={{ color: 'black' }}>
            Date of birth:
          </InputLabel>
          <Controller
            name="date_of_birth"
            control={control}
            render={({ field }) => (
              <TextField
                id="date_of_birth"
                type="date"
                onChange={(e) => setValue('date_of_birth', e.target.value)}
                sx={{ width: '300px' }}
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
          <InputLabel htmlFor="sin" sx={{ color: 'black' }}>
            Social Insurance Number (SIN) (used for CRA income disclosure):
          </InputLabel>
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
          <Upload applicationType="spouse" />
        </FormGroup>
        <FormGroup>
          <ConsentPersonal name="consent_personal" required={true} />
        </FormGroup>
        <FormGroup>
          <ConsentTax name="consent_tax" required={true} />
        </FormGroup>
        <Button
          variant="contained"
          type="submit"
          sx={{
            fontSize: '1.35rem',
            backgroundColor: '#003154',
            paddingX: '30px',
            paddingY: '10px'
          }}
        >
          Submit Application
        </Button>
      </form>
    </FormProvider>
  );
};

export default SpouseForm;
