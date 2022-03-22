import React from 'react';
import jwt_decode from 'jwt-decode';
import Form from '../components/Form';
import { useKeycloak } from '@react-keycloak/web';
import Layout from '../components/Layout';
import RebateTable from '../components/RebateTable';

const FormPage = () => {
  const { keycloak } = useKeycloak();
  // we can validate the token server side
  const decoded = jwt_decode(keycloak.token);

  return (
    <div>
      Hello BCeID {decoded.preferred_username}{' '}
      <Layout>
        <RebateTable />
        <Form />
      </Layout>
    </div>
  );
};

export default FormPage;
