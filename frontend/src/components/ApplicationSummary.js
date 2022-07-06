import React from 'react';
import { useQuery } from 'react-query';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import DetailsTable from './DetailsTable';
import { useKeycloak } from '@react-keycloak/web';
import INeedHelp from './INeedHelp';
import Loading from './Loading';
import Button from '@mui/material/Button';

const ApplicationSummary = ({ id, applicationType = '' }) => {
  const axiosInstance = useAxios();
  const { keycloak } = useKeycloak();
  const idp = keycloak.tokenParsed.identity_provider;
  const detailUrl =
    applicationType === 'household'
      ? `/api/spouse-application/${id}`
      : `/api/application-form/${id}`;
  const queryFn = () =>
    axiosInstance.current.get(detailUrl).then((response) => {
      return response.data;
    });
  const { data, isLoading, isError, error } = useQuery(
    ['application', id],
    queryFn
  );

  if (isLoading) {
    return <Loading open={true} />;
  }
  if (isError) {
    return <p>{error.message}</p>;
  }
  const typeForConfirmation =
    data.application_type === 'household'
      ? data.status === 'household_initiated'
        ? 'primary_household'
        : 'secondary_household'
      : 'individual';
  let nextSteps;
  let confirmMessage;
  switch (typeForConfirmation) {
    case 'primary_household':
      confirmMessage =
        'You’ve started a household application for a passenger vehicle rebate';
      nextSteps = (
        <>
          <p>
            Your spouse will receive an email to complete this application.
            You'll also receive a copy of this email at {data.email}
          </p>

          <p>
            Once your spouse has submitted their part of the application you’ll
            get an email reply with the result of your application within 3
            weeks. If approved the email will tell you your maximum rebate
            amount. You have one year to use the rebate from the date of
            approval.
          </p>
        </>
      );
      break;
    case 'secondary_household':
      confirmMessage = 'Success! You’ve applied for a passenger vehicle rebate';
      nextSteps = (
        <p>
          The primary applicant will get an email reply with the result of your
          application within 3 weeks.
        </p>
      );
      break;
    case 'individual':
      confirmMessage = 'Success! You’ve applied for a passenger vehicle rebate';
      nextSteps = (
        <p>
          You’ll get an email reply with the result of your application within 3
          weeks. If approved the email will tell you your maximum rebate amount.
          You have one year to use the rebate from the date of approval.
        </p>
      );
      break;
    default:
      nextSteps = '';
      break;
  }
  return (
    <Box>
      <h2>{confirmMessage}</h2>
      <p>
        Print this page for your records.
        {(typeForConfirmation === 'primary_household' ||
          typeForConfirmation === 'individual') && (
          <>
            {' '}
            You'll also receive an email confirmation of your application at{' '}
            {data.email}
          </>
        )}
      </p>
      <h2>Next steps</h2>
      {nextSteps}
      <INeedHelp
        helpText="
        Email us if you have questions or need help updating any of the
        information you’ve submitted."
      />
      <h2>What you submitted</h2>
      <DetailsTable data={{ ...data, idp }} />
      <h2>Other rebate offers for you</h2>
      <p>
        <a href="https://goelectricbc.gov.bc.ca/">
          Return to the Go Electric site to learn about other rebate offers.
        </a>
      </p>
      <Button
        className="logout-button"
        variant="contained"
        sx={{
          fontSize: '1.35rem',
          backgroundColor: '#003154',
          paddingX: '30px',
          paddingY: '10px'
        }}
        onClick={() => {
          keycloak.logout();
        }}
      >
        Log out
      </Button>
    </Box>
  );
};
export default ApplicationSummary;
