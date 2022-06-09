import React from 'react';

import ApplicationSummary from '../components/ApplicationSummary';
export default {
  title: 'ITVR/ConfirmationSummary',
  component: ApplicationSummary
};

const data = {
  id: '332vdFaugEWXTuex',
  sin: '******544',
  created: '2022-06-01T19:00:37.512469-07:00',
  status: 'submitted',
  last_name: 'Tester',
  first_name: 'TestPerson',
  middle_names: '',
  email: 'test@gov.bc.ca',
  address: '345 Fake St',
  city: 'Victoria',
  postal_code: 'V8P2N5',
  drivers_licence: '1234567',
  date_of_birth: '1999-01-01',
  tax_year: 2020,
  application_type: 'individual',
  consent_personal: true,
  consent_tax: true
};

// const Template = (args) => <ApplicationSummary {...args} />;

// export const Individual = Template.bind({});
// Individual.args = {
//   ...data
// };
// export const HouseholdSecondary = Template.bind({});
// HouseholdSecondary.args = {
//   data: {
//     ...data,
//     application_type: 'household'
//   }
// };

// export const HouseholdPrimary = Template.bind({});
// HouseholdPrimary.args = {
//   data: {
//     ...data,
//     application_type: 'household',
//     status: 'household_initiated'
//   }
// };
