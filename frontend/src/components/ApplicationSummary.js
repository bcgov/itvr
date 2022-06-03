import React from 'react';
import { useQuery } from 'react-query';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import DetailsTable from './DetailsTable';
import { useKeycloak } from '@react-keycloak/web';

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
    return <p>Loading...</p>;
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
      nextSteps = `Your spouse will receive an email at trcook77@gmail.com to complete this application. You'll also receive a copy of this email at ${data.email}`;
      break;
    case 'secondary_household':
      confirmMessage = 'Success! You’ve applied for a passenger vehicle rebate';
      nextSteps = `Your spouse will receive an email at trcook77@gmail.com to complete this application. You'll also receive a copy of this email at ${data.email}`;
      break;
    case 'individual':
      confirmMessage = 'Success! You’ve applied for a passenger vehicle rebate';
      nextSteps = `You’ll get an email reply with the result of your application within 3 weeks. If approved the email will tell you your maximum rebate amount. You have one year to use the rebate from the date of approval.`;
      break;
    default:
      nextSteps = '';
      break;
  }
  return (
    <Box>
      <h2>{confirmMessage}</h2>
      <p>
        Print this page for your records. You'll also receive an email
        confirmation of your application at {data.email || 'no email'}
      </p>
      <h2>Next steps</h2>
      <p> {nextSteps} </p>
      <h2>I need help</h2>
      <p>
        Email us if you have questions or need help updating any of the
        information you’ve submitted. ​
      </p>
      <ul>
        <li>
          <a href="mailto:ZEVPrograms@gov.bc.ca">ZEVPrograms@gov.bc.ca</a>
        </li>
      </ul>
      <h2>What you submitted</h2>
      <DetailsTable data={{ ...data, idp }} />
      <h2>Other rebate offers for you</h2>
      <p>
        <a href="https://goelectricbc.gov.bc.ca/">
          Return to the Go Electric site to learn about other rebate offers.
        </a>
      </p>
    </Box>
  );
};
export default ApplicationSummary;
