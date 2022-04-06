import React from 'react';
import { withRHF } from './hooks/withRHF';
import FileDropArea from '../components/upload/FileDropArea';

export default {
  title: 'ITVR/FileDropArea',
  component: FileDropArea,
  decorators: [withRHF(true)],
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => <FileDropArea {...args} />;

export const Default = Template.bind({});
Default.args = {};
