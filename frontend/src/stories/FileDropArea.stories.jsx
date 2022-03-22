import React from 'react';
import { within, userEvent } from '@storybook/testing-library';

import FileDropArea from '../components/upload/FileDropArea';

export default {
  title: 'FileDropArea',
  component: FileDropArea,
  parameters: {
    // More on Story layout: https://storybook.js.org/docs/react/configure/story-layout
    layout: 'fullscreen'
  }
};

const Template = (args) => <FileDropArea {...args} />;

// More on interaction testing: https://storybook.js.org/docs/react/writing-tests/interaction-testing
export const NoFiles = Template.bind({});
NoFiles.args = {};

// export const LoggedIn = Template.bind({});
// LoggedIn.play = async ({ canvasElement }) => {
//   const canvas = within(canvasElement);
//   const loginButton = await canvas.getByRole('button', { name: /Log in/i });
//   await userEvent.click(loginButton);
// };
