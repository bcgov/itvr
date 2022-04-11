import React from 'react';
import { useQuery } from 'react-query';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import DetailsTable from './DetailsTable';

const ApplicationFormDetails = (props) => {
  const { id } = props;
  const axiosInstance = useAxios();
  const queryFn = () =>
    axiosInstance.current
      .get(`/api/application-form/${id}`)
      .then((response) => response.data);

  const { data, isLoading, isError, error } = useQuery(
    ['application', id],
    queryFn
  );

  if (isLoading) {
    <p>Loading...</p>;
  }
  if (isError) {
    <p>{error.message}</p>;
  }

  return (
    <Box>
      <h3>Individual Application Confirmation</h3>
      <p>
        Print this page for your records. You will also receive an email
        confirmation at {data.email}
      </p>
      <DetailsTable data={data} />
    </Box>
  );
};
export default ApplicationFormDetails;
