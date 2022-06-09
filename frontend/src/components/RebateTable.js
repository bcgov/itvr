import React from 'react';
import Box from '@mui/material/Box';

const RebateTable = () => {
  const date = new Date();
  // get the date as a string
  const month = date.getMonth();
  let taxYear = date.getFullYear();
  if (month < 6) {
    // if its earlier than July 1
    // jan = 0, feb = 1, mar = 2, apr = 3, may = 4, june = 5, july = 6
    taxYear -= 2;
  } else {
    // if its july or later
    taxYear -= 1;
  }
  const rebateAmounts = {
    hybrid: { A: '$2,000', B: '$1,000', C: '$500', D: 'No rebate' },
    ev: { A: '$4,000', B: '$2,000', C: '$1,000', D: 'No rebate' }
  };
  const showTable = (tableType) => {
    return (
      <table
        className={
          tableType === 'large'
            ? 'rebate-table'
            : 'rebate-table rebate-table-small'
        }
      >
        <tbody>
          <tr>
            <th>Individual Income</th>
            <th>Household Income</th>
            {(tableType === 'ev' || tableType === 'hybrid') && (
              <th>Rebate amounts</th>
            )}
            {tableType === 'large' && (
              <>
                <th>Rebate for plug-in hybrids with range less than 85 km</th>
                <th>
                  Rebate for battery electric and long-range plug-in hybrids
                </th>
              </>
            )}
          </tr>
          <tr>
            <td>Less than $80,000</td>
            <td>$125,000 or less</td>
            {(tableType === 'ev' || tableType === 'hybrid') && (
              <td>{rebateAmounts[tableType]['A']}</td>
            )}
            {tableType === 'large' && (
              <>
                <td>{rebateAmounts['hybrid']['A']}</td>
                <td>{rebateAmounts['ev']['A']}</td>
              </>
            )}
          </tr>
          <tr>
            <td>$80,001 - 90,000</td>
            <td>$125,001 - 145,000</td>
            {(tableType === 'ev' || tableType === 'hybrid') && (
              <td>{rebateAmounts[tableType]['B']}</td>
            )}
            {tableType === 'large' && (
              <>
                <td>{rebateAmounts['hybrid']['B']}</td>
                <td>{rebateAmounts['ev']['B']}</td>
              </>
            )}
          </tr>
          <tr>
            <td>$90,001 - 100,000</td>
            <td>$145,001 - 165,000</td>
            {(tableType === 'ev' || tableType === 'hybrid') && (
              <td>{rebateAmounts[tableType]['C']}</td>
            )}
            {tableType === 'large' && (
              <>
                <td>{rebateAmounts['hybrid']['C']}</td>
                <td>{rebateAmounts['ev']['C']}</td>
              </>
            )}
          </tr>
          <tr>
            <td>$100,001 and above</td>
            <td>$165,001 and above</td>
            {(tableType === 'ev' || tableType === 'hybrid') && (
              <td>{rebateAmounts[tableType]['D']}</td>
            )}
            {tableType === 'large' && (
              <>
                <td>{rebateAmounts['hybrid']['D']}</td>
                <td>{rebateAmounts['ev']['D']}</td>
              </>
            )}
          </tr>
        </tbody>
      </table>
    );
  };
  return (
    <div>
      <h3>Choose your rebate application type: individual or household</h3>
      <h4>You can apply for a rebate as an individual or as a household.</h4>
      <h5> To apply as a household, you must:</h5>
      <ul>
        <li>Be married or living in a marriage-like relationship</li>
        <li>Live in the same home as your spouse or common law partner</li>
      </ul>
      <p>
        Your individual or combined household total annual income sets your
        rebate amount. Your income will be verified with the CRA based on your{' '}
        {taxYear} notice of assessment (NOA) line 15000.
      </p>
      <p> Use the table to determine the best application type for you.</p>
      <Box sx={{ display: { xs: 'None', md: 'block' } }}>
        {showTable('large')}
      </Box>
      <Box sx={{ display: { xs: 'block', md: 'None' } }}>
        <h6 className="rebate-table-title">
          Rebate for plug-in hybrid vehicles with range less than 85 km
        </h6>
        {showTable('hybrid')}
        <h6 className="rebate-table-title">
          Rebate for battery electric and long-range plug-in hybrid vehicles
        </h6>
        {showTable('ev')}
      </Box>
    </div>
  );
};

export default RebateTable;
