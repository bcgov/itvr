import React from 'react';
import { FormProvider, useForm, Controller } from 'react-hook-form';
import { useNavigate } from 'react-router-dom';
import { useMutation, useQueryClient } from 'react-query';
import FormGroup from '@mui/material/FormGroup';
import Button from '@mui/material/Button';
import TextField from '@mui/material/TextField';
import InputLabel from '@mui/material/InputLabel';
import ConsentPersonal from './ConsentPersonal';
import ConsentTax from './ConsentTax';
import FileDropArea from './upload/FileDropArea';
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
  const queryClient = useQueryClient();
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
    mutation.mutate(data, {
      onSuccess: (data, variables, context) => {
        const id = data.data.id;
        queryClient.setQueryData(['application', id], data.data);
        navigate(`/details/${id}`);
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

  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit, onError)}>
        <FormGroup>
          <Box my={5}>
            <FormControl>
              <FormLabel className="label" id="application_type" sx={{ mb: 1 }}>
                If you can receive a larger rebate applying as a household your
                spouse or common law partner will need to complete a portion of
                this application to confirm their identity and provide their CRA
                income disclosure consent. Instructions will be sent to them by
                email.
              </FormLabel>
              <RadioGroup
                aria-labelledby="application_type"
                name="application_type"
                defaultValue={defaultValues.application_type}
              >
                <FormControlLabel
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
                          <b>Apply as a household,</b> enter your spouse or
                          common law partner's email address below.
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

            <Box mt={2}>
              <sup>3</sup>
              <sub>
                <b>Household:</b> a person or group of persons who occupy the
                same dwelling and do not have a usual place of residence
                elsewhere in Canada or abroad. The dwelling may be either a
                collective dwelling or a private dwelling.
              </sub>
            </Box>
            <Box mt={2}>
              <sup>4</sup>
              <sub>
                <b>Spouse:</b> someone of the same or opposite gender who has
                one of the following types of relationship to you (1) they are
                married to you (2) they are living in a marriage-like
                relationship with you.
              </sub>
            </Box>
          </Box>
        </FormGroup>
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
          {errors?.email?.type === 'required' && (
            <p className="error">Email Address cannot be blank</p>
          )}
          <InputLabel htmlFor="email">Email Address:</InputLabel>
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
          {errors?.address?.type === 'required' && (
            <p className="error">Street Address cannot be blank</p>
          )}
          <InputLabel htmlFor="address">Street Address:</InputLabel>
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
        <FormGroup>
          {errors?.city?.type === 'required' && (
            <p className="error">City cannot be blank</p>
          )}
          <InputLabel htmlFor="city">City:</InputLabel>
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
        <FormGroup>
          {errors?.postal_code?.type === 'validate' && (
            <p className="error">Not a valid Postal Code</p>
          )}
          <InputLabel htmlFor="postal_code">Postal Code (optional):</InputLabel>
          <Controller
            name="postal_code"
            control={control}
            render={({ field }) => (
              <TextField
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
              validate: (inputtedSin) => {
                return isSINValid(inputtedSin);
              }
            }}
          />
        </FormGroup>
        <FormGroup>
          {errors?.drivers_licence?.type === 'validate' && (
            <p className="error">Not a valid B.C. Driver's Licence Number</p>
          )}
          <InputLabel htmlFor="drivers_licence">
            B.C. Driver's Licence Number:
          </InputLabel>
          <Controller
            name="drivers_licence"
            control={control}
            render={({ field }) => (
              <TextField
                id="drivers_licence"
                inputProps={{ maxLength: 8 }}
                onChange={(e) => setValue('drivers_licence', e.target.value)}
              />
            )}
            rules={{
              validate: (inputtedLicence) => {
                if (
                  !inputtedLicence ||
                  (inputtedLicence.length !== 7 && inputtedLicence.length !== 8)
                ) {
                  return false;
                }
                const regex = /^\d+$/;
                if (!regex.test(inputtedLicence)) {
                  return false;
                }
                return true;
              }
            }}
          />
        </FormGroup>
        <FormGroup>
          <Box>
            Upload an image (jpg or png) of your B.C. Driver's Licence (photo
            side) and a secondary piece of ID &nbsp;
            <a href="/identificationExamples" target="_blank">
              (see examples):
            </a>
          </Box>
          {errors?.documents?.type === 'twoOrMore' && (
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

export default Form;
