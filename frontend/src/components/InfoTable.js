import React , { useState } from 'react';
import Box from '@mui/material/Box';
import Table from '@mui/material/Table';
import TableBody from '@mui/material/TableBody';
import TableCell from '@mui/material/TableCell';
import TableContainer from '@mui/material/TableContainer';
import TableRow from '@mui/material/TableRow';

const InfoTable = ({ householdInfo = {}, kcToken = '' }) => {
  const [errors, seterrors] = useState(false);
  function createData(name, answer) {
    if (answer === null) {
      seterrors(true);
    }
    return { name, answer };
  }

  const rows = kcToken
    ? [
        createData('Your last name (surname):', kcToken.family_name),
        createData('First name (given name):', kcToken.given_name),
        createData('Date of birth:', kcToken.birthdate),
        createData('Street address:', kcToken.street_address),
        createData('City:', kcToken.locality),
        kcToken.postal_code && createData('Postal code:', kcToken.postal_code)
      ]
    : [
        createData('Street address:', householdInfo.address),
        createData('City:', householdInfo.city),
        createData('Postal Code:', householdInfo.postal_code)
      ];

  return (
    <>
      {kcToken && (
        <div>
          <p className="info-table-text">
          Your name, date of birth and address below has been provided from your
          BC Services Card app.
        </p>
        {errors  === true && (
            <p className="error">Your BC Services Card app has provided incomplete information. 
            Please correct this with your BC Services Card app first before using this application form.</p>
          )}
        </div>

      )}
      <TableContainer>
        <Table sx={{ minWidth: 100, maxWidth: 700 }} aria-label="simple table">
          <TableBody>
            {rows.map((row) => (
              <TableRow
                key={row.name}
                sx={{
                  border: '0 !important'
                }}
              >
                <TableCell
                  component="th"
                  scope="row"
                  sx={{
                    verticalAlign: 'top',
                    width: { xs: '150px', sm: '250px', md: '400px' },
                    border: 0,
                    padding: 0,
                    fontSize: {
                      xs: '1rem',
                      sm: '1.2rem',
                      md: '1.35rem'
                    }
                  }}
                >
                  {row.name}
                </TableCell>
                <TableCell
                  align="left"
                  sx={{
                    verticalAlign: 'top',
                    border: 0,
                    padding: 0,
                    fontSize: { xs: '1rem', sm: '1.2rem', md: '1.35rem' },
                    color: 'text.disabled'
                  }}
                >
                  {row.answer}
                </TableCell>
              </TableRow>
            ))}
          </TableBody>
        </Table>
      </TableContainer>
    </>
  );
};
export default InfoTable;
