import React from 'react';
import {
  BrowserRouter, Routes, Route, Navigate,
} from 'react-router-dom';
import { useKeycloak } from '@react-keycloak/web';

import Home from '../pages';
import FormPage from '../pages/Form';
import Admin from '../pages/admin';

const RequireAuth = ({ children, redirectTo }) => {
  const { keycloak } = useKeycloak();
  console.log('checking keycloak');
  return keycloak.authenticated ? children : <Navigate to={redirectTo} />;
};

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<Home />} />
      <Route
        path="/admin"
        element={(
          <RequireAuth redirectTo="/">
            <Admin />
          </RequireAuth>
        )}
      />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
