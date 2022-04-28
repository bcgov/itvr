import React from 'react';
import Layout from '../components/Layout';
import ApplicationSummary from '../components/ApplicationSummary';
import { useParams } from 'react-router-dom';

const ApplicationSummaryPage = () => {
  const { id } = useParams();
  return (
    <div>
      <Layout>
        <ApplicationSummary id={id} />
      </Layout>
    </div>
  );
};

export default ApplicationSummaryPage;
