import React, { useEffect, useState, useRef } from 'react';
import SpouseForm from '../components/SpouseForm';
import Layout from '../components/Layout';
import { useKeycloak } from '@react-keycloak/web';
import { useSearchParams } from 'react-router-dom';
import { Helmet } from 'react-helmet';

const HouseholdFormPage = () => {
  const [searchParams] = useSearchParams();
  const householdApplicationId = searchParams.get('q');
  const [numberOfErrors, setNumberOfErrors] = useState(0);
  const [errorsExistCounter, setErrorsExistCounter] = useState(0);
  const errorMessageRef = useRef(null);
  const { keycloak } = useKeycloak();

  useEffect(() => {
    if (numberOfErrors > 0) {
      errorMessageRef.current.scrollIntoView({ behavior: 'smooth' });
    }
  }, [errorsExistCounter]);

  return (
    <div>
      <Helmet>
        <title>
          Passenger Vehicle Rebate Application Form – CleanBC Go Electric
        </title>
      </Helmet>
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
