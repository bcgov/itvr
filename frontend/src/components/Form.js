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

const Form = () => {
  const queryClient = useQueryClient();
  const methods = useForm({
    defaultValues
  });
  const { control, handleSubmit, register, watch } = methods;
  const axiosInstance = useAxios();
  const navigate = useNavigate();
  const mutation = useMutation((data) => {
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
  const onSubmit = (data) =>
    mutation.mutate(data, {
      onSuccess: (data, variables, context) => {
        const id = data.data.id;
        queryClient.setQueryData(['application', id], data.data);
        navigate(`/details/${id}`);
      }
    });

  return (
    <FormProvider {...methods}>
      <form onSubmit={handleSubmit(onSubmit)}>
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
