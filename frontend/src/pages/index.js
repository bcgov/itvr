import React from 'react';
import Layout from '../components/Layout';
import { Helmet } from 'react-helmet';
import IndividualLogin from '../components/IndividualLogin';

function Index() {
  return (
    <div className="app">
      <Helmet>
        <title>Passenger Vehicle Rebate Log In – CleanBC Go Electric</title>
      </Helmet>
      <Layout>
        <IndividualLogin />
      </Layout>
    </div>
  );
}

export default Index;
