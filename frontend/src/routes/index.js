import React from 'react';
import { BrowserRouter, Routes, Route, Navigate } from 'react-router-dom';
import { useKeycloak } from '@react-keycloak/web';

import HomePage from '../pages';
import FormPage from '../pages/Form';
import AdminPage from '../pages/admin';
import DetailsPage from '../pages/Details';
import HouseholdPage from '../pages/Household';
import HouseholdFormPage from '../pages/HouseholdForm';

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
        path="/eligibility"
        element={
          <RequireAuth redirectTo="/">
            <FormPage />
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
      <Route path="/household" element={<HouseholdPage />} />
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
    </Routes>
  </BrowserRouter>
);

export default AppRouter;
