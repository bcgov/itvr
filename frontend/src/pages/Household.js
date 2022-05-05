import React from 'react';
import BottomBanner from '../components/BottomBanner';
import Layout from '../components/Layout';
import { useSearchParams } from 'react-router-dom';

const HouseholdPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const householdApplicationId = searchParams.get('q');
  const title = (
    <>
      <h3>Complete your rebate application for your household</h3>
      <h5>What you will need to complete this application</h5>
    </>
  );
  const applicationText = (
    <div>
      <ul>
        <li>A Basic BCeID.</li>
        <li>An image of your B.C. Driver's Licence or B.C. Services Card.</li>
        <li>An image of a secondary piece of ID.</li>
        <li>
          Your Social Insurance Number and CRA income disclosure consent to
          confirm your income.
        </li>
      </ul>
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
      </div>
    </Layout>
  );
};

export default HouseholdPage;
