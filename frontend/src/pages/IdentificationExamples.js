import React from 'react';
import Layout from '../components/Layout';
import IdentificationExamples from '../components/IdentificationExamples';
import {Helmet} from "react-helmet";

const IdentificationExamplesPage = () => {
  return (
    <div>
      <Helmet>
        <title>Passenger vehicle rebate identification requirements – CleanBC Go Electric</title>
      </Helmet>
      <Layout>
        <IdentificationExamples />
      </Layout>
    </div>
  );
};

export default IdentificationExamplesPage;
