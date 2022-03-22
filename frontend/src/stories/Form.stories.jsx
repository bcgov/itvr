import React from 'react';
import { FormProvider, useForm } from 'react-hook-form';
import Form, { defaultValues } from '../components/Form';

export default {
  title: 'ITVR/Rebate Form',
  component: Form,
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => {
  const methods = useForm({
    defaultValues
  });
  return (
    <FormProvider {...methods}>
      <Form {...args} />
    </FormProvider>
  );
};

export const RebateForm = Template.bind({});
RebateForm.args = {};
