import React from 'react';

import HouseholdPage from '../pages/Household';

export default {
  title: 'ITVR/Household',
  component: HouseholdPage
};

const Template = (args) => <HouseholdPage {...args} />;
export const Default = Template.bind({});
