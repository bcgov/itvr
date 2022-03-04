import axios from 'axios';
import React, { useState } from 'react';
import ApplicationFormPage from './components/ApplicationFormPage';
import ROUTES_APPLICATION from './routes';

const ApplicationFormContainer = () => {
  const [loading, setLoading] = useState(false);
  const [details, setDetails] = useState({});

  const handleInputChange = (event) => {
    const { value, name } = event.target;
    setDetails({
      ...details,
      [name]: value,
    });
  };
  const handleSubmit = () => {
    axios.post(ROUTES_APPLICATION.SAVE, { details })
      .then((response) => { console.log(response); });
  };

  return (
    <div>
      <ApplicationFormPage
        loading={loading}
        handleInputChange={handleInputChange}
        details={details}
        handleSubmit={handleSubmit}
      />
    </div>
  );
};

export default ApplicationFormContainer;
