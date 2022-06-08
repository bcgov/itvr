import React from 'react';
import BottomBanner from '../components/BottomBanner';
import Layout from '../components/Layout';
import { useSearchParams } from 'react-router-dom';
import INeedHelp from '../components/INeedHelp';

const HouseholdPage = () => {
  const [searchParams] = useSearchParams();
  const householdApplicationId = searchParams.get('q');
  const title = (
    <>
      <h2>What you will need to complete this application</h2>
    </>
  );
  const applicationText = (
    <div>
      <h3>A Basic BCeID.</h3>
      <p>
        Used to confirm your income. To give consent to the Canada Revenue
        Agency (CRA) to disclose your income information.
      </p>
      <h3>BC Services Card app or Basic BCeID</h3>
      <p>Used to confirm your identity.</p>
      <p>
        The{' '}
        <a href="https://www2.gov.bc.ca/gov/content/governments/government-id/bcservicescardapp">
          BC Services Card app{' '}
        </a>
        is the simplest method to log in and confirm your identity.
      </p>
      <p>
        You can also log in with a{' '}
        <a href="https://www.bceid.ca/register/basic/account_details.aspx?type=regular&eServiceType=basic">
          Basic BCeID account
        </a>
        . If you log in with BCeID you will need to upload images of your BC
        Driver’s Licence or BC Services Card and a secondary piece of ID.{' '}
        <a href="/identificationExamples" target="_blank">
          Learn more about ID requirements.
        </a>
      </p>
    </div>
  );

  return (
    <Layout>
      <div>
        <div className="whats-needed-spouse">
          {title}
          {applicationText}
        </div>
        <BottomBanner
          eligible={true}
          text="Complete your rebate application"
          type="spouse"
          householdApplicationId={householdApplicationId}
        />
        <INeedHelp
          helpText="Contact Go Electric if you have questions about the rebate process or
        your application:"
        />
      </div>
    </Layout>
  );
};

export default HouseholdPage;
