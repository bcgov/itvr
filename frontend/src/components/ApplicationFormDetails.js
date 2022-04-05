import React from 'react';
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
const rows = [
  createData('Application ID:', 1234567),
  createData('Last name / surname:', 'Smith'),
  createData('First name / given name:', 'John'),
  createData('Middle name(s):', 'David'),
  createData('Email address:', 'jdsmith@shaw.ca'),
  createData('Date of birth:', '19700906'),
  createData('Street address:', '910 Government St.'),
  createData('City:', 'Victoria BC'),
  createData('Postal Code:', 'V8W 3Y8'),
  createData('Social Insurance Number (SIN):', '******123'),
  createData("B.C. Driver's Licence number:", 'DL:2222222'),
  createData('Tax Year:', '2020'),
  createData(
    'Consent to Disclosure and Storage of, and Access to, Personal Information:',
    'BCEIDJSMITH 20220504 12:04:01 PST'
  ),
  createData(
    'Consent to Disclosure of Information from Income Tax Records:',
    'BCEIDJSMITH 20220504 12:04:01 PST'
  )
];

const ApplicationFormDetails = (props) => {
  console.log(props);
  return (
    <Box>
      <h3>Individual Application Confirmation</h3>
      <p>
        Print this page for your records. You will also receive an email
        confirmation at jdsmith@shaw.ca
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
