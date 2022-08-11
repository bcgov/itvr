import React from 'react';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';
import Paper from '@mui/material/Paper';

function createData(name, answer, elementId) {
  return { name, answer, elementId };
}

function createConsentValue(consent, displayName, timestamp, idp) {
  const timestampSplit = timestamp.split('T');
  const date = timestampSplit[0];
  const time = timestampSplit[1].split('.')[0];
  const offset = timestampSplit[1].split('-')[1];
  const authType = idp === 'bcsc' ? 'BCSC' : 'BCEID';
  let pacificTimeType = 'Pacific Time';
  if (offset === '07:00') {
    pacificTimeType = 'PDT';
  } else if (offset === '08:00') {
    pacificTimeType = 'PST';
  }
  if (consent) {
    return (
      authType +
      '\\' +
      displayName +
      ' ' +
      date +
      ' ' +
      time +
      ' ' +
      pacificTimeType
    );
  }
}

const DetailsTable = ({ data }) => {
  let rows = [
    createData(
      'Application ID:',
      data.application_id || data.id,
      'application_id'
    ),
    createData('Last name / surname:', data.last_name, 'last_name'),
    createData('First name / given name:', data.first_name, 'first_name'),
    createData('Middle name(s):', data.middle_names, 'middle_names'),
    createData('Email address:', data.email, 'email'),
    createData('Date of birth:', data.date_of_birth, 'date_of_birth'),
    createData('Street address:', data.address, 'address'),
    createData('City:', data.city, 'city'),
    createData('Postal Code:', data.postal_code, 'postal_code'),
    createData('Social Insurance Number (SIN):', data.sin, 'sin'),
    data.drivers_licence &&
      createData(
        "BC Driver's Licence number:",
        data.drivers_licence,
        'drivers_licence'
      ),
    createData('Tax Year:', data.tax_year, 'tax_year'),
    createData(
      'Consent to Disclosure and Storage of, and Access to, Personal Information:',
      createConsentValue(
        data.consent_personal,
        data.displayName,
        data.created,
        data.idp
      ),
      'consent_personal'
    ),
    createData(
      'Consent to Disclosure of Information from Income Tax Records:',
      createConsentValue(
        data.consent_tax,
        data.displayName,
        data.created,
        data.idp
      ),
      'consent_tax'
    )
  ];
  rows = rows.filter((r) => r);
  return (
    <TableContainer component={Paper} sx={{ boxShadow: 0 }}>
      <Table
        sx={{ minWidth: { md: 650 }, border: 0 }}
        aria-label="simple table"
      >
        <TableBody>
          {rows.map((row) => {
            if (row.answer) {
              return (
                <TableRow key={row.name} sx={{ border: 0 }}>
                  <TableCell
                    component="th"
                    scope="row"
                    sx={{
                      border: 0,
                      width: { xs: '40%', md: '25%' },
                      fontSize: { xs: '.9rem', md: '1.35rem' }
                    }}
                  >
                    <b>{row.name}</b>
                  </TableCell>
                  <TableCell
                    id={row.elementId}
                    align="left"
                    sx={{ border: 0, fontSize: { xs: '1rem', md: '1.35rem' } }}
                    className="application-details-table-answer"
                    style={{
                      verticalAlign: 'top'
                    }}
                  >
                    {row.answer}
                  </TableCell>
                </TableRow>
              );
            }
          })}
        </TableBody>
      </Table>
    </TableContainer>
  );
};
export default DetailsTable;
