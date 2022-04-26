import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(name, answer) {
  return { name, answer };
}

function createConsentValue(consent, firstName, lastName, timestamp) {
  const timestampSplit = timestamp.split("T");
  const date = timestampSplit[0];
  const time = timestampSplit[1].split(".")[0];
  if(consent) {
    return ("BCEID\\" + firstName.charAt(0).toUpperCase() + lastName.toUpperCase() + " " + date + " " + time + " PST");
  }
}

const DetailsTable = ({ data }) => {
  const rows = [
    createData('Application ID:', data.id),
    createData('Last name / surname:', data.last_name),
    createData('First name / given name:', data.first_name),
    createData('Middle name(s):', data.middle_names),
    createData('Email address:', data.email),
    createData('Date of birth:', data.date_of_birth),
    createData('Street address:', data.address),
    createData('City:', data.city),
    createData('Postal Code:', data.postal_code),
    createData('Social Insurance Number (SIN):', data.sin),
    createData("B.C. Driver's Licence number:", data.drivers_licence),
    createData('Tax Year:', data.tax_year),
    createData(
      'Consent to Disclosure and Storage of, and Access to, Personal Information:',
      createConsentValue(data.consent_personal, data.first_name, data.last_name, data.created)
    ),
    createData(
      'Consent to Disclosure of Information from Income Tax Records:',
      createConsentValue(data.consent_tax, data.first_name, data.last_name, data.created)
    )
  ];
  return (
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
  );
};
export default DetailsTable;