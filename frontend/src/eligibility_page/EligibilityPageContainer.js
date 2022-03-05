import React, { useState } from 'react';
import EligibilityPage from './components/EligibilityPage';

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

  return (
    <div>
      <EligibilityPage />
    </div>
  );
};

export default ApplicationFormContainer;
