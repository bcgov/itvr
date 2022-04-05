import React from 'react';
import Layout from '../components/Layout';
import ApplicationFormDetails from '../components/ApplicationFormDetails';
import { useParams } from 'react-router-dom';

const ApplicationDetailsPage = () => {
  const { id } = useParams();
  return (
    <div>
      <Layout>
        <ApplicationFormDetails id={id} />
      </Layout>
    </div>
  );
};

export default ApplicationDetailsPage;
