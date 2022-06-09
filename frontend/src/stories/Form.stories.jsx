import React from 'react';
import Form from '../components/Form';
import SpouseForm from '../components/SpouseForm';

export default {
  title: 'ITVR/RebateForm',
  component: Form,
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => <Form {...args} />;
export const IndividualForm = Template.bind({});
IndividualForm.args = {};

// const SpouseTemplate = (args) => <SpouseForm {...args} />;
// export const HouseholdForm = SpouseTemplate.bind({});
// HouseholdForm.args = {};
