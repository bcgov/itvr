import React from 'react';
import { Route, Redirect } from 'react-router-dom';
import { useKeycloak } from '@react-keycloak/web';

const PrivateRoute = ({
  component,
  ...rest
}) => {
  const { keycloak } = useKeycloak();

  return (
    <Route
      {...rest}
      render={(props) => (keycloak.authenticated ? (
        <component {...props} />
      ) : (
        <Redirect
          to={{
            pathname: '/',
            state: { from: props.location },
          }}
        />
      ))}
    />
  );
};

export default PrivateRoute;
