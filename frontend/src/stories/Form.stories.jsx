import React from 'react';
import Form from '../components/Form';

export default {
  title: 'ITVR/Rebate Form',
  component: Form,
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => <Form {...args} />;
export const RebateForm = Template.bind({});
RebateForm.args = {};
