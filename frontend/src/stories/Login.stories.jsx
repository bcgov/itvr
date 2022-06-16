import React from 'react';

import HouseholdLogin from '../pages/HouseholdLogin';
import IndividualLogin from '../components/IndividualLogin';

export default {
  title: 'ITVR/Login',
  component: IndividualLogin
};

const TemplateIndividual = (args) => <IndividualLogin />;
export const Individual = TemplateIndividual.bind({});

const TemplateHousehold = (args) => <HouseholdLogin />;
export const Household = TemplateHousehold.bind({});
