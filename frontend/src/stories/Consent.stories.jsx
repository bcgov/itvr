import React from 'react';

import ConsentPersonal from '../components/ConsentPersonal';
import ConsentTax from '../components/ConsentTax';

export default {
  title: 'Consent',
  component: ConsentPersonal,
  parameters: {
    layout: 'fullscreen'
  }
};

const TemplatePersonal = (args) => <ConsentPersonal {...args} />;

export const PersonalConsentBox = TemplatePersonal.bind({});
PersonalConsentBox.args = {};

const TemplateTax = (args) => <ConsentTax {...args} />;

export const TaxConsentBox = TemplateTax.bind({});
TaxConsentBox.args = {};
