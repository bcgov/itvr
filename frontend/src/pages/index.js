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
            <title>Passenger vehicle rebate log in – CleanBC Go Electric</title>
            <title>Passenger vehicle rebate application form – CleanBC Go Electric</title>
            <title>Passenger vehicle rebate identification requirements – CleanBC Go Electric</title>
            <title>Passenger vehicle rebate application confirmation  – CleanBC Go Electric</title>
        </Helmet>
      <Layout>
        <EligibilityPageContainer />
      </Layout>
      {keycloak.authenticated && (
        <button type="button" onClick={() => keycloak.logout()}>
          Logout
        </button>
      )}
    </div>
  );
}

export default Index;
