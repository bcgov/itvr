import React from 'react';

import ApplicationConsent from '../components/ApplicationConsent';

export default {
  title: 'Consent',
  component: ApplicationConsent,
  parameters: {
    layout: 'fullscreen'
  }
};

const Template = (args) => <ApplicationConsent {...args} />;

export const Consent = Template.bind({});
