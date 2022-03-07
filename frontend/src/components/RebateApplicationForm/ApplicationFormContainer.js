import React, { useState } from 'react';
import ApplicationFormPage from './ApplicationFormPage';
import useAxios from '../../utils/axiosHook';

const ApplicationFormContainer = () => {
  const [loading] = useState(false);
  const [details, setDetails] = useState({});
  // const axiosInstance = useAxios({withCredentials: true});
  const axiosInstance = useAxios();

  const handleInputChange = (event) => {
    const { value, name } = event.target;
    setDetails({
      ...details,
      [name]: value,
    });
  };
  const handleSubmit = () => {
    axiosInstance.current.post('/api/application-form', { details })
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
