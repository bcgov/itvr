import React, { useEffect, useState, useRef } from 'react';
import jwt_decode from 'jwt-decode';
import Form from '../components/Form';
import Layout from '../components/Layout';
import RebateTable from '../components/RebateTable';
import { useKeycloak } from '@react-keycloak/web';
import {Helmet} from "react-helmet";

const FormPage = () => {
  const { keycloak } = useKeycloak();
  // we can validate the token server side
  const decoded = jwt_decode(keycloak.token);
  console.log(decoded);

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
      <Helmet>
        <title>Passenger vehicle rebate application form – CleanBC Go Electric</title>
      </Helmet>
      <Layout>
      {numberOfErrors > 0 && (
        <span className="error" ref={errorMessageRef}>
          Errors below, please ensure all fields are complete
        </span>
      )}
      <RebateTable />
      <Form
        setNumberOfErrors={setNumberOfErrors}
        setErrorsExistCounter={setErrorsExistCounter}
      />
      </Layout>
    </div>
    
  );
};

export default FormPage;
