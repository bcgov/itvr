import axios from 'axios';
import React, { useEffect, useRef, useState } from 'react';
import ApplicationFormPage from './components/ApplicationFormPage';
import ROUTES_APPLICATION from './routes';

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
    console.log(details);
    axios.post(ROUTES_APPLICATION.SAVE, { details })
      .then((response) => { console.log(response); });
  };
  useEffect(() => {
    setLoading(true);
    // do an axios get for whatever informaion we need to retrieve for the form to be filled
    // axios.get(ROUTES_APPLICATION.LIST)
    //   .then((response)=>{
    //     console.log(response.data)
    //     setDetails(response.data)})
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
