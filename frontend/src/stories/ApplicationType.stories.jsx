import React from 'react';
// import { withRHF } from './hooks/withRHF';
import ApplicationType from '../components/ApplicationType';

export default {
  title: 'ITVR/ApplicationType',
  component: ApplicationType,
  //   decorators: [withRHF(true)],
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => <ApplicationType {...args} />;

export const Default = Template.bind({});
