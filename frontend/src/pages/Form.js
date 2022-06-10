import React, { useEffect, useState, useRef } from 'react';
import Form from '../components/Form';
import Layout from '../components/Layout';
import RebateTable from '../components/RebateTable';
import { Helmet } from 'react-helmet';

const FormPage = () => {
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
        <h2>Apply for a passenger vehicle rebate</h2>
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
