import React from 'react';
import Layout from '../components/Layout';
import ApplicationSummaryTable from '../components/ApplicationSummaryTable';
import { useParams } from 'react-router-dom';

const ApplicationSummaryPage = () => {
  const { id } = useParams();
  return (
    <div>
      <Layout>
        <ApplicationSummaryTable id={id} />
      </Layout>
    </div>
  );
};

export default ApplicationSummaryPage;
