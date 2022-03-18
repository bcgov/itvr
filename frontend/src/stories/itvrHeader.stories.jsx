import React from "react";

import Header from "../components/Header";

export default {
  title: "Header",
  component: Header,
};

// export const EligibilityHeader = () => <Header pageTitle="Test" />;

const Template = (args) => <Header {...args} />;
export const test = Template.bind({});
