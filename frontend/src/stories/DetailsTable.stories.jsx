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
    modified: '2022-06-01T19:00:37.512501-07:00',
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
    doc1: 'http://minio:9000/itvr/docs/savepdf_xjXa0q1.png?AWSAccessKeyId=minioadmin&Signature=OtYacKFXfJcCe3UW4EpghxqSh7Y%3D&Expires=1654138889',
    doc2: 'http://minio:9000/itvr/docs/Font-Settings_Bnwxs6B.png?AWSAccessKeyId=minioadmin&Signature=nsEHXKqLeBP%2BIGgR5F%2FJXoZ2kp0%3D&Expires=1654138889',
    application_type: 'individual',
    consent_personal: true,
    consent_tax: true,
    user: 1
  }
};
