import React from 'react';

import HouseholdLogin from '../pages/HouseholdLogin';

export default {
  title: 'ITVR/HouseholdLogin',
  component: HouseholdLogin
};

const Template = (args) => <HouseholdLogin {...args} />;
export const Default = Template.bind({});
