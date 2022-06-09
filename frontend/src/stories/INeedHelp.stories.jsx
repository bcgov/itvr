import React from 'react';

import INeedHelp from '../components/INeedHelp';

export default {
  title: 'ITVR/INeedHelp',
  component: INeedHelp
};

const Template = (args) => <INeedHelp {...args} />;
export const Summary = Template.bind({});
Summary.args = {
  helpText:
    'Email us if you have questions or need help updating any of the information you’ve submitted.'
};

export const Login = Template.bind({});
Login.args = {
  helpText:
    'Contact Go Electric if you have questions about the rebate process or your application:'
};
