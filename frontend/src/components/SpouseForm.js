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
import { getDateWithYearOffset, isSINValid } from '../utility';
import LockIcon from '@mui/icons-material/Lock';
import Upload from './upload/Upload';
import Loading from './Loading';
import { useKeycloak } from '@react-keycloak/web';
import InfoTable from './InfoTable';
import { addTokenFields, checkBCSC } from '../keycloak';
import { AdapterDateFns } from '@mui/x-date-pickers/AdapterDateFns';
import { LocalizationProvider } from '@mui/x-date-pickers/LocalizationProvider';
import DateBoxes from './DateBoxes';

const maxDate = getDateWithYearOffset(new Date(), -16);
const minDate = getDateWithYearOffset(maxDate, -100);

export const defaultValues = {
  application: '',
  sin: '',
  first_name: '',
  last_name: '',
  middle_names: '',
  address: '',
  city: '',
  postal_code: '',
  date_of_birth: maxDate,
  documents: [],
  consent_personal: false,
  consent_tax: false
};

const SpouseForm = ({
  id,
  setNumberOfErrors,
  setErrorsExistCounter,
  setSameUser
}) => {
  const [loading, setLoading] = useState(false);
  const [applicationBlocked, setApplicationBlocked] = useState(false);
  const { keycloak } = useKeycloak();
  const kcToken = keycloak.tokenParsed;
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
  const [DOB, setDOB] = useState(maxDate);
  const axiosInstance = useAxios();
  let bcscMissingFields = [];
  if (kcToken.identity_provider === 'bcsc') {
    bcscMissingFields = checkBCSC(kcToken);
  }
  const queryFn = () =>
    axiosInstance.current
      .get(`/api/application-form/${id}/household`)
      .then((response) => response.data);

  const { data, isLoading, isError, error } = useQuery({
    queryKey: ['spouse-application', id],
    queryFn: queryFn,
    retry: (failureCount, error) => {
      const errorResponse = error.response;
      if (
        errorResponse &&
        errorResponse.data &&
        errorResponse.data.error === 'same_user'
      ) {
        return false;
      } else if (
        errorResponse &&
        errorResponse.data &&
        errorResponse.data.error === 'application_advanced'
      ) {
        return false;
      } else if (failureCount >= 2) {
        return false;
      }
      return true;
    },
    refetchOnWindowFocus: false
  });

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
  const onDobChange = (dob) => {
    setValue('date_of_birth', dob);
    setDOB(dob);
  };
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
        let refinedData = data.data;
        if (kcToken.identity_provider === 'bcsc') {
          refinedData = addTokenFields(data.data, kcToken);
        }
        queryClient.setQueryData(
          ['spouse-application', applicationId],
          refinedData
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

  const cancelApplication = () => {
    setLoading(true);
    axiosInstance.current
      .patch(`/api/application-form/${id}`, { status: 'cancelled' })
      .then((response) => {
        setApplicationBlocked(true);
        setLoading(false);
      })
      .catch((error) => {
        setLoading(false);
      });
  };

  if (isLoading) {
    return <Loading open={true} />;
  }
  if (applicationBlocked) {
    return (
      <p>
        This application has already been completed, or it has been cancelled.
      </p>
    );
  }
  if (isError) {
    const errorResponse = error.response;
    if (
      errorResponse &&
      errorResponse.data &&
      errorResponse.data.error === 'same_user'
    ) {
      setSameUser({
        error: true,
        logoutUri: `${window.location.origin}/household?q=${id}`
      });
    } else if (
      errorResponse &&
      errorResponse.data &&
      errorResponse.data.error === 'application_advanced'
    ) {
      setApplicationBlocked(true);
    }
    return <p>{error.message}</p>;
  }
  const { address, city, postal_code: postalCode, status } = data;
  return (
    <FormProvider {...methods}>
      <Loading open={loading} />
      <form onSubmit={handleSubmit(onSubmit, onError)}>
        <h2>Apply for a passenger vehicle rebate pre-approval</h2>
        <Box sx={{ display: 'inline' }}>
          <h3 id="form-submission-title">
            Complete your household rebate application <LockIcon />
          </h3>
          <span> secure form submission</span>
        </Box>
        <p className="info-table-text">
          The address information below has been provided from your household
          application and must match your identification.
        </p>
        <InfoTable householdInfo={data} />
        {kcToken.identity_provider === 'bcsc' ? (
          <InfoTable kcToken={kcToken} bcscMissingFields={bcscMissingFields} />
        ) : (
          <>
            <FormGroup sx={{ mt: '20px' }}>
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

            <FormGroup sx={{ mt: '20px' }}>
              <InputLabel htmlFor="date_of_birth" sx={{ color: 'black' }}>
                Date of birth:
              </InputLabel>
              <Controller
                name="date_of_birth"
                control={control}
                render={({ field }) => (
                  <LocalizationProvider dateAdapter={AdapterDateFns}>
                    <Box
                      sx={{
                        display: 'flex',
                        flexDirection: 'row',
                        paddingTop: '20px'
                      }}
                    >
                      <DateBoxes
                        maxDate={maxDate}
                        minDate={minDate}
                        value={DOB}
                        onChange={onDobChange}
                      />
                    </Box>
                  </LocalizationProvider>
                )}
              />
            </FormGroup>
          </>
        )}
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
              validate: (inputtedSIN) => {
                return isSINValid(inputtedSIN);
              }
            }}
          />
        </FormGroup>
        {kcToken.identity_provider !== 'bcsc' && (
          <FormGroup sx={{ mt: '20px' }}>
            <Upload errors={errors} applicationType="spouse" />
          </FormGroup>
        )}
        <FormGroup sx={{ mt: '20px' }}>
          <ConsentPersonal name="consent_personal" required={true} />
        </FormGroup>
        <FormGroup sx={{ mt: '20px' }}>
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
          disabled={loading || bcscMissingFields.length > 0}
        >
          Submit Application
        </Button>
      </form>
      {status === 'household_initiated' && (
        <Box>
          <p>
            If you are unable to complete this application click Cancel
            Application. This will notify the primary applicant and enable them
            to start a new application.
          </p>
          <Button
            variant="contained"
            sx={{
              fontSize: '1.35rem',
              backgroundColor: 'white',
              color: 'red',
              border: '1px solid red',
              paddingX: '30px',
              paddingY: '10px'
            }}
            disabled={loading}
            onClick={cancelApplication}
          >
            Cancel Application
          </Button>
        </Box>
      )}
    </FormProvider>
  );
};

export default SpouseForm;
