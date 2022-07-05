import { useKeycloak } from '@react-keycloak/web';
import Box from '@mui/material/Box';

const HouseholdLoginError = ({ id }) => {
  const { keycloak } = useKeycloak();
  if (keycloak.authenticated) {
    return (
      <Box>
        <h2>Log in error</h2>
        <p>
          You must use your own BC Services Card app or Basic BCeID account to
          log in.
        </p>
        <p>
          You cannot use the same log in credentials as the applicant to
          complete your household rebate application.
        </p>
        <p>
          Click the Log out button and log in using your own BC Services Card
          app or Basic BCeID account.
        </p>
        <button
          type="button"
          className="button"
          onClick={() => {
            keycloak.logout({
              redirectUri: `${window.location.origin}/household?q=${id}`
            });
          }}
        >
          Log out
        </button>
      </Box>
    );
  }
  return null;
};

export default HouseholdLoginError;
