import React from 'react';

import ApplicationSummaryTable from '../components/ApplicationSummaryTable';

export default {
  title: 'ITVR/ApplicationFormDetails',
  component: ApplicationSummaryTable
};

const Template = (args) => <ApplicationSummaryTable {...args} />;
export const Default = Template.bind({});
