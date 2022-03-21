import React from 'react';

import ApplicationConsent from '../components/ApplicationConsent';

export default {
  title: 'Consent',
  component: ApplicationConsent,
  parameters: {
    // More on Story layout: https://storybook.js.org/docs/react/configure/story-layout
    layout: 'fullscreen'
  }
};

const Template = (args) => <ApplicationConsent {...args} />;

// More on interaction testing: https://storybook.js.org/docs/react/writing-tests/interaction-testing
export const Consent = Template.bind({});
