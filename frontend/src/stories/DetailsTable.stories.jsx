import React from 'react';

import DetailsTable from '../components/DetailsTable';

export default {
  title: 'ITVR/DetailsTable',
  component: DetailsTable
};

const Template = (args) => <DetailsTable {...args} />;
export const Default = Template.bind({});
Default.args = {
  data: {
    id: '332vdFaugEWXTuex',
    sin: '******544',
    created: '2022-06-01T19:00:37.512469-07:00',
    status: 'submitted',
    last_name: 'Aro',
    first_name: 'Naomi',
    middle_names: '',
    email: 'naomi.aro@gov.bc.ca',
    address: '345 Fake St',
    city: 'Victoria',
    postal_code: 'V8P2N5',
    drivers_licence: '1234567',
    date_of_birth: '1999-01-01',
    tax_year: 2020,
    application_type: 'individual',
    consent_personal: true,
    consent_tax: true
  }
};
