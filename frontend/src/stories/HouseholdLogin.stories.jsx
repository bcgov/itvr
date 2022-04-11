import React from 'react';

import Household from '../pages/Household';

export default {
  title: 'ITVR/Household',
  component: Household
};

const Template = (args) => <Household {...args} />;
export const Default = Template.bind({});
