import React from 'react';
import Form from '../components/Form';

export default {
  title: 'ITVR/RebateForm',
  component: Form,
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => <Form {...args} />;
export const Default = Template.bind({});
Default.args = {};
