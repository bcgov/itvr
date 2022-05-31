import React from 'react';
import Layout from '../components/Layout';
import ApplicationSummary from '../components/ApplicationSummary';
import { useParams } from 'react-router-dom';
import {Helmet} from "react-helmet";

const ApplicationSummaryPage = () => {
  const { id } = useParams();
  return (
    <div>
      <Helmet>
        <title>Passenger vehicle rebate application confirmation  – CleanBC Go Electric</title>
      </Helmet>
      <Layout>
        <ApplicationSummary id={id} />
      </Layout>
    </div>
  );
};

export default ApplicationSummaryPage;
