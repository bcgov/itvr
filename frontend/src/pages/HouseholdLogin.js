import React from 'react';
import BottomBanner from '../components/BottomBanner';
import Layout from '../components/Layout';
import { useSearchParams } from 'react-router-dom';
import INeedHelp from '../components/INeedHelp';
import BCEIDLogin from '../components/BCEIDLogin';
const HouseholdLogin = () => {
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
      <h3>BC Services Card app</h3>
      <p>Used to confirm your identity.</p>
      <p>
        The{' '}
        <a href="https://www2.gov.bc.ca/gov/content/governments/government-id/bcservicescardapp">
          BC Services Card app{' '}
        </a>
        is the simplest method to log in and confirm your identity.
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
        <BCEIDLogin type="household" />
        <INeedHelp
          helpText="Contact Go Electric if you have questions about the rebate process or
        your application:"
        />
      </div>
    </Layout>
  );
};

export default HouseholdLogin;
