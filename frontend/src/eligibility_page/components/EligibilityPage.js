import Box from '@mui/material/Box';
import React from 'react';
import EligibilityQuestions from './EligibilityQuestions';
import RebateTable from '../RebateTable';

import BottomBanner from '../BottomBanner';

const EligibilityPage = (props) => {
  const { taxYear, questions, setQuestions, handleCheckboxChange, eligible } =
    props;

  return (
    <div>
      <div>
        <p>
          Rebates of up to $4,000 are available from the B.C. Government towards
          the purchase of a new electric vehicle. Your individual or household
          income determines the rebate amount.
        </p>
        <h3>How it works</h3>
        <div>
          <ol>
            <li>
              Complete the following eligibility questions and online
              application process.
            </li>
            <li>You will be notified by email your rebate amount.</li>
            <li>
              The rebate is associated with your B.C. Driver's Licence number.
              You will need to present your driver's licence at the car
              dealership to receive the rebate discount at the time of vehicle
              purchase.
            </li>
          </ol>
        </div>
        <RebateTable taxYear={taxYear} />

        <h3>Determine your eligibility for a rebate</h3>
        {questions.map((question, index) => (
          <EligibilityQuestions
            question={question.question}
            index={index}
            setQuestions={setQuestions}
            handleCheckboxChange={handleCheckboxChange}
          />
        ))}
        <div id="whats-needed">
          <h3>What you will need to complete this application</h3>
          <ul>
            <li>
              Your Driver's Licence number to be associated with the rebate.
            </li>
            <li>
              A Basic BCeID, an image of your B.C. Driver's Licence and a
              secondary piece of ID to upload.
            </li>
            <li>
              Your Social Insurance Number and CRA income disclosure consent to
              confirm your income.
            </li>
          </ul>
          For a household application your spouse or common law partner will
          also need to confirm their identity and provide CRA income disclosure
          consent, they do not require a driver's licence.
        </div>
      </div>
      <BottomBanner eligible={eligible} taxYear={taxYear} />
    </div>
  );
};

export default EligibilityPage;
