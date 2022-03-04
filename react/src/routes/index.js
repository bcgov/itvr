import * as React from 'react';
import { BrowserRouter as Router, Redirect, Route } from 'react-router-dom';

import { useKeycloak } from '@react-keycloak/web';

import HomePage from '../pages';
import FormPage from '../pages/Form';
import AdminPage from '../pages/admin';

import PrivateRoute from './private';

const AppRouter = () => {
  const { initialized } = useKeycloak();

  if (!initialized) {
    return <div>Loading...</div>;
  }

  return (
    <Router>
      {/* <Redirect from="/" to="/home" /> */}
      <Route path="/" component={HomePage} />
      <PrivateRoute path="/form" component={FormPage} />
      <PrivateRoute path="/admin" component={AdminPage} />
    </Router>
  );
};

export default AppRouter;
