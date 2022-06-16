import { useKeycloak } from '@react-keycloak/web';
import React from 'react';
import Layout from '../components/Layout';
import { Helmet } from 'react-helmet';
import IndividualLogin from '../components/IndividualLogin';

function Index() {
  const { keycloak } = useKeycloak();

  return (
    <div className="app">
      <Helmet>
        <title>Passenger Vehicle Rebate Log In – CleanBC Go Electric</title>
      </Helmet>
      <Layout>
        <IndividualLogin />
      </Layout>
      {keycloak.authenticated && (
        <button
          type="button"
          onClick={() => {
            keycloak.logout();
          }}
        >
          Logout
        </button>
      )}
    </div>
  );
}

export default Index;
