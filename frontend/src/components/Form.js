import React, { useState } from 'react';
import { FormProvider, useForm, Controller } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from 'react-query';
import FormGroup from '@mui/material/FormGroup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import ConsentPersonal from './ConsentPersonal';
import ConsentTax from './ConsentTax';
import useAxios from '../utils/axiosHook';
import SpouseEmail from './SpouseEmail';
import FormControlLabel from '@mui/material/FormControlLabel';
import Typography from '@mui/material/Typography';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import Box from '@mui/material/Box';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import { isAgeValid, isSINValid } from '../utility';
import LockIcon from '@mui/icons-material/Lock';
import InputAdornment from '@mui/material/InputAdornment';
import OutlinedInput from '@mui/material/OutlinedInput';
import Upload from './upload/Upload';
import Loading from './Loading';
import { useKeycloak } from '@react-keycloak/web';
import InfoTable from './InfoTable';
import { addTokenFields } from '../keycloak';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import { DatePicker } from '@mui/x-date-pickers/DatePicker';

export const defaultValues = {
  sin: '',
  first_name: '',
  last_name: '',
  middle_names: '',
  email: '',
  address: '',
  city: '',
  postal_code: '',
  date_of_birth: '',
  drivers_licence: '',
  documents: [],
  consent_personal: false,
  consent_tax: false,
  application_type: 'individual',
  spouse_email: ''
};

const Form = ({ setNumberOfErrors, setErrorsExistCounter }) => {
  const [loading, setLoading] = useState(false);
  const [DOB, setDOB] = useState(new Date());
  const queryClient = useQueryClient();
  const { keycloak } = useKeycloak();
  const kcToken = keycloak.tokenParsed;
  const methods = useForm({
    defaultValues
  });
  const {
    control,
    handleSubmit,
    register,
    watch,
    formState: { errors },
    setValue
  } = methods;
  const axiosInstance = useAxios();
  const navigate = useNavigate();
  const mutation = useMutation((data) => {
    const formData = new FormData();
    for (const [key, value] of Object.entries(data)) {
      if (key === 'documents') {
        formData.append('doc1', value[0]);
        formData.append('doc2', value[1]);
      } else if (key === 'postal_code' && value.length === 7) {
        formData.append(key, value.replace(/[ -]/, ''));
      } else {
        formData.append(key, value);
      }
    }
    return axiosInstance.current.post('/api/application-form', formData, {
      headers: { 'Content-Type': 'multipart/form-data' }
    });
  });
  const onSubmit = (data) => {
    setNumberOfErrors(0);
    setLoading(true);
    if (kcToken.identity_provider !== 'bcsc') {
      data = {
        ...data,
        date_of_birth: data.date_of_birth.toISOString().slice(0, 10)
      };
    }
    mutation.mutate(data, {
      onSuccess: (data, variables, context) => {
        const id = data.data.id;
        let refinedData = data.data;
        if (kcToken.identity_provider === 'bcsc') {
          refinedData = addTokenFields(data.data, kcToken);
        }
        queryClient.setQueryData(['application', id], refinedData);
        navigate(`/details/${id}`);
      }
    });
  };

  const checkDLStatus = (dl) => {
    const detailUrl = `/api/application-form/check_status/?drivers_license=${dl}`;
    return axiosInstance.current.get(detailUrl);
  };

  const onError = (errors) => {
    setLoading(false);
    const numberOfErrors = Object.keys(errors).length;
    setNumberOfErrors(numberOfErrors);
    if (numberOfErrors > 0) {
      setErrorsExistCounter((prev) => {
        return prev + 1;
      });
    }
  };

  return (
    <FormProvider {...methods}>
      <Loading open={loading} />
      <form onSubmit={handleSubmit(onSubmit, onError)}>
        <h5>Application process for households</h5>
        <p>
          Your spouse will need to complete a part of the application.
          Instructions will be sent to them by email after you complete your
          part of the application below.
        </p>
        <p>
          Your spouse will need their own BC Services Card app or Basic BCeID
          account. Your ID will be used to confirm that you and your spouse live
          at the same address.
        </p>
        <FormGroup>
          <Box mb={5}>
            <FormControl>
              <FormLabel
                className="label"
                id="application_type"
                sx={{ mb: 1 }}
              ></FormLabel>
              <RadioGroup
                aria-labelledby="application_type"
                name="application_type"
                defaultValue={defaultValues.application_type}
              >
                <FormControlLabel
                  sx={{ color: 'black' }}
                  value="individual"
                  control={
                    <Radio
                      name="application_type"
                      {...register('application_type')}
                    />
                  }
                  label={
                    <Typography color="textPrimary" fontWeight="bold">
                      {'Apply as an individual'}
                    </Typography>
                  }
                />
                <FormControlLabel
                  value="household"
                  control={
                    <Radio
                      name="application_type"
                      {...register('application_type')}
                    />
                  }
                  label={
                    <Typography color="textPrimary">
                      {
                        <>
                          {' '}
                          <b>Apply as a household</b>
                        </>
                      }
                    </Typography>
                  }
                />
              </RadioGroup>
            </FormControl>

            {watch('application_type') === 'household' && (
              <SpouseEmail name="spouse_email" />
            )}
          </Box>
        </FormGroup>
        <Box sx={{ display: 'inline' }}>
          <h3 id="form-submission-title">
            Your application information <LockIcon />
          </h3>
          <span> secure form submission</span>
        </Box>
        {kcToken.identity_provider === 'bcsc' ? (
          <InfoTable kcToken={kcToken} />
        ) : (
          <>
            <FormGroup sx={{ mt: '20px' }}>
              {errors?.last_name?.type === 'required' && (
                <p className="error">Last Name cannot be blank</p>
              )}
              <InputLabel htmlFor="last_name" sx={{ color: 'black' }}>
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
            <FormGroup sx={{ mt: '20px' }}>
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
            <FormGroup sx={{ mt: '20px' }}>
              <InputLabel htmlFor="middle_names" sx={{ color: 'black' }}>
                Middle Names(s) (optional):
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
            <FormGroup sx={{ mt: '20px' }}>
              {errors?.date_of_birth?.type === 'validate' && (
                <p className="error">
                  Date of birth cannot be blank and you must be 16 years or
                  older to request a rebate, please check the date of birth
                  entered.
                </p>
              )}
              <InputLabel htmlFor="date_of_birth" sx={{ color: 'black' }}>
                Date of birth:
              </InputLabel>
              <Controller
                name="date_of_birth"
                control={control}
                render={({ field }) => (
                  <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <DatePicker
                      disableFuture
                      openTo="year"
                      views={['year', 'month', 'day']}
                      value={DOB}
                      format="YYYY-MM-DD"
                      onChange={(newDate) => {
                        setValue('date_of_birth', newDate);
                        setDOB(newDate);
                      }}
                      renderInput={(params) => <TextField {...params} />}
                    />
                  </LocalizationProvider>
                )}
                rules={{
                  validate: (inputtedDOB) => {
                    return isAgeValid(inputtedDOB, 16);
                  }
                }}
              />
            </FormGroup>
            <FormGroup sx={{ mt: '20px' }}>
              {errors?.address?.type === 'required' && (
                <p className="error">Street Address cannot be blank</p>
              )}
              <InputLabel htmlFor="address" sx={{ color: 'black' }}>
                Street address:
              </InputLabel>
              <Controller
                name="address"
                control={control}
                render={({ field }) => (
                  <TextField
                    id="address"
                    inputProps={{ maxLength: 250 }}
                    onChange={(e) => setValue('address', e.target.value)}
                  />
                )}
                rules={{ required: true }}
              />
            </FormGroup>
            <FormGroup sx={{ mt: '20px' }}>
              {errors?.city?.type === 'required' && (
                <p className="error" sx={{ color: 'black' }}>
                  City cannot be blank
                </p>
              )}
              <InputLabel htmlFor="city" sx={{ color: 'black' }}>
                City:
              </InputLabel>
              <Controller
                name="city"
                control={control}
                render={({ field }) => (
                  <TextField
                    id="city"
                    inputProps={{ maxLength: 250 }}
                    onChange={(e) => setValue('city', e.target.value)}
                  />
                )}
                rules={{ required: true }}
              />
            </FormGroup>
            <FormGroup sx={{ mt: '20px' }}>
              {errors?.postal_code?.type === 'validate' && (
                <p className="error">Not a valid Postal Code</p>
              )}
              <InputLabel htmlFor="postal_code" sx={{ color: 'black' }}>
                Postal code (optional):
              </InputLabel>
              <Controller
                name="postal_code"
                control={control}
                render={({ field }) => (
                  <TextField
                    sx={{ width: '300px' }}
                    id="postal_code"
                    inputProps={{ maxLength: 7 }}
                    onChange={(e) => setValue('postal_code', e.target.value)}
                  />
                )}
                rules={{
                  validate: (inputtedPostalCode) => {
                    if (inputtedPostalCode) {
                      if (
                        inputtedPostalCode.length !== 6 &&
                        inputtedPostalCode.length !== 7
                      ) {
                        return false;
                      }
                      const regex = /[A-Za-z]\d[A-Za-z][ -]?\d[A-Za-z]\d/;
                      if (!regex.test(inputtedPostalCode)) {
                        return false;
                      }
                    }
                    return true;
                  }
                }}
              />
            </FormGroup>
          </>
        )}
        <FormGroup sx={{ mt: '20px' }}>
          {errors?.email?.type === 'required' && (
            <p className="error">Email Address cannot be blank</p>
          )}
          <InputLabel htmlFor="email" sx={{ color: 'black' }}>
            Email Address:
          </InputLabel>
          <Controller
            name="email"
            type="email"
            control={control}
            render={({ field }) => (
              <TextField
                id="email"
                inputProps={{ maxLength: 250 }}
                onChange={(e) => setValue('email', e.target.value)}
              />
            )}
            rules={{ required: true }}
          />
        </FormGroup>
        <FormGroup sx={{ mt: '20px' }}>
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
              validate: (inputtedSin) => {
                return isSINValid(inputtedSin);
              }
            }}
          />
        </FormGroup>
        <FormGroup sx={{ mt: '20px' }}>
          {errors?.drivers_licence?.type === 'dlFormat' && (
            <p className="error">Not a valid B.C. Driver's Licence Number</p>
          )}
          {errors?.drivers_licence?.type === 'dlExists' && (
            <p className="error">
              This driver's licence number has already been submitted or issued
              a rebate, or we cannot check your licence.
            </p>
          )}
          <InputLabel htmlFor="drivers_licence" sx={{ color: 'black' }}>
            BC Driver's Licence number (used for redeeming your rebate):
          </InputLabel>
          <Controller
            name="drivers_licence"
            control={control}
            render={({ field }) => (
              <OutlinedInput
                id="drivers_licence"
                inputProps={{
                  maxLength: 8
                }}
                startAdornment={
                  <InputAdornment position="start">DL: </InputAdornment>
                }
                onChange={(e) => setValue('drivers_licence', e.target.value)}
              />
            )}
            rules={{
              validate: {
                dlFormat: (inputtedLicence) => {
                  if (
                    !inputtedLicence ||
                    (inputtedLicence.length !== 7 &&
                      inputtedLicence.length !== 8)
                  ) {
                    return false;
                  }
                  const regex = /^\d+$/;
                  if (!regex.test(inputtedLicence)) {
                    return false;
                  }
                  return true;
                },
                dlExists: async (inputtedLicence) => {
                  try {
                    setLoading(true);
                    const response = await checkDLStatus(inputtedLicence);
                    if (response.data.drivers_license_valid === 'false') {
                      return false;
                    }
                  } catch (error) {
                    return false;
                  }
                  return true;
                }
              }
            }}
          />
        </FormGroup>
        {kcToken.identity_provider !== 'bcsc' && (
          <FormGroup sx={{ mt: '20px' }}>
            <Upload errors={errors} />
          </FormGroup>
        )}
        <FormGroup sx={{ mt: '20px' }}>
          <ConsentPersonal name="consent_personal" required={true} />
        </FormGroup>
        <FormGroup sx={{ mt: '20px' }}>
          <ConsentTax
            name="consent_tax"
            required={true}
            applicationType="individual"
          />
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
          disabled={loading}
        >
          Submit Application
        </Button>
      </form>
    </FormProvider>
  );
};

export default Form;
