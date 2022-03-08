import React from 'react';
import {
  BrowserRouter, Routes, Route, Navigate,
} from 'react-router-dom';
import { useKeycloak } from '@react-keycloak/web';

import HomePage from '../pages';
import FormPage from '../pages/Form';
import AdminPage from '../pages/admin';

const RequireAuth = ({ children, redirectTo }) => {
  const { keycloak } = useKeycloak();
  return keycloak.authenticated ? children : <Navigate to={redirectTo} />;
};

const AppRouter = () => (
  <BrowserRouter>
    <Routes>
      <Route path="/" element={<HomePage />} />
      <Route
        path="/form"
        element={(
          <RequireAuth redirectTo="/">
            <FormPage />
          </RequireAuth>
        )}
      />
      <Route
        path="/admin"
        element={(
          <RequireAuth redirectTo="/">
            <AdminPage />
          </RequireAuth>
        )}
      />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
