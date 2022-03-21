import React from 'react';
import { within, userEvent } from '@storybook/testing-library';

import Form from '../components/Form';

export default {
  title: 'Rebate Form',
  component: Form,
  parameters: {
    // More on Story layout: https://storybook.js.org/docs/react/configure/story-layout
    layout: 'fullscreen'
  }
};

const Template = (args) => <Form {...args} />;

// More on interaction testing: https://storybook.js.org/docs/react/writing-tests/interaction-testing
export const RebateForm = Template.bind({});
// NoFiles.args = {
//   uploadFiles: []
// };

// export const LoggedIn = Template.bind({});
// LoggedIn.play = async ({ canvasElement }) => {
//   const canvas = within(canvasElement);
//   const loginButton = await canvas.getByRole('button', { name: /Log in/i });
//   await userEvent.click(loginButton);
// };
