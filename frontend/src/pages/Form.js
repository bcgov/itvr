import React from 'react';
import jwt_decode from "jwt-decode";
import ApplicationFormContainer from '../components/RebateApplicationForm/ApplicationFormContainer';
import { useKeycloak } from '@react-keycloak/web';

const Form = () => {
  const { keycloak } = useKeycloak();
  // we can validate the token server side when they submit the form.
  const decoded = jwt_decode(keycloak.token);

  return (
    <div>
      Hello BCeID {decoded.preferred_username}
      <ApplicationFormContainer/>
    </div>
  );
};

export default Form;
