import React from 'react';

const INeedHelp = (props) => {
  const { helpText } = props;
  return (
    <>
      <h3 id="help-email">I need help</h3>
      <p>{helpText}</p>
      <ul>
        <li>
          Email <a href="mailto:ZEVPrograms@gov.bc.ca">ZEVPrograms@gov.bc.ca</a>
        </li>
      </ul>
    </>
  );
};
export default INeedHelp;
