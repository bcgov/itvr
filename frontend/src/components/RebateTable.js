import React from 'react';

const RebateTable = (props) => {
  const { year } = props;
  return (
    <div>
      <h4>Rebate Application Type (Individual or Household)</h4>
      <p>
        If your total individual income was $100,000 or less or your total
        household income was $165,000 or less you are eligible for a rebate at
        the following rates:
      </p>
      <table>
        <tbody>
          <tr>
            <th>Individual Income</th>
            <th>Household Income</th>
            <th>
              Rebate Amount Range
              <sup>1</sup>
            </th>
          </tr>
          <tr>
            <td>Less than $80,000</td>
            <td>Less than $125,000</td>
            <td>$2,000 - $4,000</td>
          </tr>
          <tr>
            <td>$80,001 - 90,000</td>
            <td>$125,001 - 145,000</td>
            <td>$1,000 - $2,000</td>
          </tr>
          <tr>
            <td>$90,001 - 100,000</td>
            <td>$145,001 - 165,000</td>
            <td>$500 - $1,000</td>
          </tr>
        </tbody>
      </table>
      <sup>1</sup>
      <sub>
        <b>Rebate Amount Range:</b> BEV (Battery Electric Vehicle) and
        long-range PHEV (Plug-in Hybrid Electric Vehicle) receive the higher
        rebate amount.
      </sub>
      <p>
        Your income will be verified with the Canada Revenue Agency based on
        your {year} notice of assessment (line 15000).
      </p>
      <sup>2</sup>
      <sub>
        <b>Tax year:</b> up until June 30 your {year} notice of assessment (NOA)
        will be used to determine your rebate amount. On July 1 it will change
        to use your {year} NOA.
      </sub>
    </div>
  );
};

export default RebateTable;
