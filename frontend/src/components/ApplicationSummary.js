import React from 'react';
import { useQuery } from 'react-query';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import DetailsTable from './DetailsTable';

const ApplicationSummary = ({ id, applicationType = '' }) => {
  const axiosInstance = useAxios();
  const detailUrl =
    applicationType === 'household'
      ? `/api/application-form/${id}/household`
      : `/api/application-form/${id}`;
  const queryFn = () =>
    axiosInstance.current.get(detailUrl).then((response) => {
      if (applicationType === 'household') {
        return {
          ...response.data,
          id: response.data.original_application.id,
          address: response.data.original_application.address,
          postal_code: response.data.original_application.postal_code,
          city: response.data.original_application.city,
          tax_year: response.data.original_application.tax_year
        };
      } else {
        return response.data;
      }
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
  console.log(data);
  return (
    <Box>
      <h3>
        {applicationType === 'household'
          ? 'Household Application'
          : 'Individual Application Confirmation'}
      </h3>
      <p>
        Print this page for your records. You will also receive an email
        confirmation at {data.email}
      </p>
      <DetailsTable data={data} />
    </Box>
  );
};
export default ApplicationSummary;
