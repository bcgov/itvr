import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';

import HomePage from '../pages';
import FormPage from '../pages/Form';
import AdminPage from '../pages/admin';
import DetailsPage from '../pages/Details';
import HouseholdLogin from '../pages/HouseholdLogin';
import HouseholdFormPage from '../pages/HouseholdForm';
import HouseholdDetails from '../pages/HouseholdDetails';
import IdentificationExamplesPage from '../pages/IdentificationExamples';
import { useKeycloak } from '@react-keycloak/web';

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
        element={
          <RequireAuth redirectTo="/">
            <FormPage />
          </RequireAuth>
        }
      />
      <Route
        path="/details/:id/household"
        element={
          <RequireAuth redirectTo="/">
            <HouseholdDetails />
          </RequireAuth>
        }
      />
      <Route
        path="/details/:id"
        element={
          <RequireAuth redirectTo="/">
            <DetailsPage />
          </RequireAuth>
        }
      />
      <Route path="/household" element={<HouseholdLogin />} />
      <Route
        path="/householdForm"
        element={
          <RequireAuth redirectTo="/">
            <HouseholdFormPage />
          </RequireAuth>
        }
      />
      <Route
        path="/admin"
        element={
          <RequireAuth redirectTo="/">
            <AdminPage />
          </RequireAuth>
        }
      />
      <Route
        path="/identificationExamples"
        element={<IdentificationExamplesPage />}
      />
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
