import React from 'react';
import Layout from '../components/Layout';
import ApplicationSummary from '../components/ApplicationSummary';
import { useParams } from 'react-router-dom';

const HouseholdSummary = () => {
  const { id } = useParams();

  return (
    <div>
      <Layout>
        <ApplicationSummary id={id} applicationType="household" />
      </Layout>
    </div>
  );
};

export default HouseholdSummary;
