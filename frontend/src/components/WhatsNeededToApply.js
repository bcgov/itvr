import React from 'react';

const WhatsNeededToApply = ({ type, applicationText, title }) => {
  return (
    <div
      className={
        type === 'individual'
          ? 'whats-needed-individual'
          : 'whats-needed-spouse'
      }
    >
      {title}
      {applicationText}
    </div>
  );
};
export default WhatsNeededToApply;
