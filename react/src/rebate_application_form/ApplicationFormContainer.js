import axios from 'axios';
import React, { useEffect, useRef, useState } from 'react';
import ApplicationFormPage from './components/ApplicationFormPage';

const ApplicationFormContainer = () => {
  const [data, setData] = useState([]);
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
    axios.post(details);
  };
  useEffect(() => {
    setLoading(true);
    // do an axios get for whatever informaion we need to retrieve for the form to be filled
    setLoading(false);
  }, []);
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
