import React, { useEffect, useState, useRef } from 'react';
import jwt_decode from 'jwt-decode';
import SpouseForm from '../components/SpouseForm';
import Layout from '../components/Layout';
import { useKeycloak } from '@react-keycloak/web';

const HouseholdFormPage = () => {
  const { keycloak } = useKeycloak();
  // we can validate the token server side
  const decoded = jwt_decode(keycloak.token);
  const householdApplicationId = keycloak.idTokenParsed.nonce;

  const [numberOfErrors, setNumberOfErrors] = useState(0);
  const [errorsExistCounter, setErrorsExistCounter] = useState(0);
  const errorMessageRef = useRef(null);

  useEffect(() => {
    if (numberOfErrors > 0) {
      errorMessageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [errorsExistCounter]);

  return (
    <div>
      Hello BCeID {decoded.preferred_username}
      <Layout>
        {numberOfErrors > 0 && (
          <span className="error" ref={errorMessageRef}>
            Errors below, please ensure all fields are complete
          </span>
        )}
        <SpouseForm
          id={householdApplicationId}
          setNumberOfErrors={setNumberOfErrors}
          setErrorsExistCounter={setErrorsExistCounter}
        />
      </Layout>
    </div>
  );
};

export default HouseholdFormPage;
