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
    id: '948b5f3d-f347-4d07-a46c-7907c3874d2f',
    create_timestamp: '2022-04-05T18:53:53.647558Z',
    create_user: 'SYSTEM',
    update_timestamp: '2022-04-05T18:53:53.647608Z',
    update_user: null,
    sin: '234234234',
    last_name: 'Aro',
    first_name: 'Naomi',
    middle_names: '',
    email: 'naomi.aro@gov.bc.ca',
    address: '345 Fake St',
    city: 'Victoria',
    postal_code: 'V8P2N5',
    drivers_licence: '1234567',
    date_of_birth: '2022-04-15',
    tax_year: 2021,
    doc1: 'http://minio:9000/itvr/docs/275764713_370797044908674_1617869606850339037_n_5j2r2mn.jpg',
    doc2: 'http://minio:9000/itvr/docs/275637215_462674682262245_3325277982481944110_n_kEk97ON.jpg',
    verified: false
  }
};
