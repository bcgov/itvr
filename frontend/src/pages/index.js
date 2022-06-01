import { useKeycloak } from '@react-keycloak/web';
import React from 'react';
import EligibilityPageContainer from '../components/Eligibility/EligibilityPageContainer';
import Layout from '../components/Layout';
import {Helmet} from "react-helmet";

function Index() {
  const { keycloak } = useKeycloak();

  return (
    <div className="app">
      <Helmet>
        <title>Passenger Vehicle Rebate Log In – CleanBC Go Electric</title>
      </Helmet>
      <Layout>
        <EligibilityPageContainer />
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
