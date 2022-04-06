import React from 'react';
import { withRHF } from './hooks/withRHF';
import ConsentPersonal from '../components/ConsentPersonal';
import ConsentTax from '../components/ConsentTax';

export default {
  title: 'ITVR/Consent',
  component: ConsentPersonal,
  decorators: [withRHF(true)],
  parameters: {
    layout: 'fullscreen'
  }
};

const TemplatePersonal = (args) => <ConsentPersonal {...args} />;

export const PersonalConsentBox = TemplatePersonal.bind({});
PersonalConsentBox.args = { name: 'consent_personal' };

const TemplateTax = (args) => <ConsentTax {...args} />;

export const TaxConsentBox = TemplateTax.bind({});
TaxConsentBox.args = { name: 'consent_tax' };
