import React from 'react';
import { useQuery } from 'react-query';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import DetailsTable from './DetailsTable';

const ApplicationSummary = ({ id, applicationType = '' }) => {
  const axiosInstance = useAxios();
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
  return (
    <Box>
      <h3>
        {data.application_type === 'household'
          ? 'Household Application'
          : 'Individual Application Confirmation'}
      </h3>
      <p>
        {data.status !== 'submitted' || data.application_type !== 'household'
          ? 'Print this page for your records. You will also receive an email confirmation at ' +
            data.email
          : 'Print this page for your records.'}
      </p>
      {data.status === 'household_initiated' && (
        <p>Your spouse will receive an email to complete this application.</p>
      )}
      <DetailsTable data={data} />
    </Box>
  );
};
export default ApplicationSummary;
