import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import React from 'react';
import EligibilityQuestions from './EligibilityQuestions';
import RebateTable from '../RebateTable';
import { useKeycloak } from '@react-keycloak/web';

const EligibilityPage = (props) => {
  const { year, questions, setQuestions, handleCheckboxChange, eligible } =
    props;
  const { keycloak } = useKeycloak();
  return (
    <div>
      <div>
        <h1>Electric Vehicle Rebates</h1>
        <h2>for Individuals and Households</h2>
      </div>
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
            <li>
              If you are eligible, a rebate code will be emailed to you that
              indicates your rebate amount.
            </li>
            <li>
              The rebate code is associated with your B.C. Driver&apos;s Licence
              number. They are both needed at the car dealership to receive the
              rebate discount at the time of vehicle purchase.
            </li>
          </ol>
        </div>
        <RebateTable year={year} />

        <h3>Determine your eligibility for a rebate</h3>
        {questions.map((question, index) => (
          <EligibilityQuestions
            question={question.question}
            index={index}
            setQuestions={setQuestions}
            handleCheckboxChange={handleCheckboxChange}
          />
        ))}
        <div className="grey-background">
          <h3>What you will need to complete this application</h3>
          <ul>
            <li>
              Your Driver's Licence number to be associated with the rebate
              code.
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
      <div id="start-application">
        <h2>Start your rebate application</h2>
        <div id="bceid-login">
          <h2>BCeID</h2>
          <button
            type="button"
            className="button"
            disabled={!eligible}
            onClick={() =>
              keycloak.login({
                idpHint: 'bceid-basic',
                redirectUri: `${window.location.origin}/form`
              })
            }
          >
            Login with BCeID
          </button>
          <div>
            <a href="">Get a Basic BCeID account</a>
            <p>
              The name associated with your BCeID account must match your legal
              first and last name on your identification documents
            </p>
          </div>
        </div>
      </div>
    </div>
  );
};

export default EligibilityPage;
