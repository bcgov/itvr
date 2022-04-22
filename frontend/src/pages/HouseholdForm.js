import React from 'react';
import jwt_decode from 'jwt-decode';
import SpouseForm from '../components/SpouseForm';
import { useKeycloak } from '@react-keycloak/web';
import Layout from '../components/Layout';
import { useSearchParams } from 'react-router-dom';

const HouseholdFormPage = () => {
  const [searchParams, setSearchParams] = useSearchParams();
  const householdApplicationId = searchParams.get('q');
  const { keycloak } = useKeycloak();
  // we can validate the token server side
  const decoded = jwt_decode(keycloak.token);

  return (
    <div>
      Hello BCeID {decoded.preferred_username}
      <Layout>
        <SpouseForm id={householdApplicationId} />
      </Layout>
    </div>
  );
};

export default HouseholdFormPage;
