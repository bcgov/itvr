import React from 'react';
import { useQuery } from 'react-query';
import useAxios from '../utils/axiosHook';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(name, answer) {
  return { name, answer };
}

const ApplicationFormDetails = (props) => {
  const { id } = props;
  const axiosInstance = useAxios();
  const enabled = true;
  const queryFn = () =>
    axiosInstance.current.get(`/api/application-form/${id}`);

  const { data } = useQuery({
    id,
    queryFn,
    enabled
  });

  const rows = [
    createData('Application ID:', data ? data.data.id : ''),
    createData('Last name / surname:', data ? data.data.last_name : ''),
    createData('First name / given name:', data ? data.data.first_name : ''),
    createData('Middle name(s):', data ? data.data.middle_names : ''),
    createData('Email address:', data ? data.data.email : ''),
    createData('Date of birth:', data ? data.data.date_of_birth : ''),
    createData('Street address:', data ? data.data.address : ''),
    createData('City:', data ? data.data.city : ''),
    createData('Postal Code:', data ? data.data.postal_code : ''),
    createData('Social Insurance Number (SIN):', data ? data.data.sin : ''),
    createData(
      "B.C. Driver's Licence number:",
      data ? data.data.drivers_licence : ''
    ),
    createData('Tax Year:', data ? data.data.tax_year : ''),
    createData(
      'Consent to Disclosure and Storage of, and Access to, Personal Information:',
      data ? data.data.consentpersonal : ''
    ),
    createData(
      'Consent to Disclosure of Information from Income Tax Records:',
      data ? data.data.consenttax : ''
    )
  ];

  return (
    <Box>
      <h3>Individual Application Confirmation</h3>
      <p>
        Print this page for your records. You will also receive an email
        confirmation at {data && data.data && data.data.email}
      </p>

      <TableContainer component={Paper} sx={{ boxShadow: 0 }}>
        <Table sx={{ minWidth: 650, border: 0 }} aria-label="simple table">
          <TableBody>
            {rows.map((row) => (
              <TableRow key={row.name} sx={{ border: 0 }}>
                <TableCell
                  component="th"
                  scope="row"
                  sx={{ border: 0, width: '25%' }}
                >
                  <b>{row.name}</b>
                </TableCell>
                <TableCell
                  align="left"
                  sx={{ border: 0 }}
                  className="application-details-table-answer"
                  style={{ verticalAlign: 'top' }}
                >
                  {row.answer}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </Box>
  );
};
export default ApplicationFormDetails;
