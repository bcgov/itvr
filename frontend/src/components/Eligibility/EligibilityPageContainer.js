import React, { useState } from 'react';
import EligibilityPage from './EligibilityPage';

const ApplicationFormContainer = () => {
  const [loading, setLoading] = useState(false);
  const [details, setDetails] = useState({});

  const date = new Date();
  // get the date as a string
  const month = date.getMonth();
  let year = date.getFullYear();
  if (month < 6) {
    // if its earlier than July 1
    // jan = 0, feb = 1, mar = 2, apr = 3, may = 4, june = 5, july = 6
    year -= 1;
  } else {
    // if its july or later
    year -= 2;
  }
  const [questions, setQuestions] = useState([
    { 'Have you previously received an electric vehicle rebate from the Government of British Columbia?': '' },
    { 'Do you reside in British Columbia and have a valid B.C. Drivers Licence?': '' },
    { 'Did you file a year tax return with the Canada Revenue Agency (CRA)?': '' },
    { 'Was your individual total income $100,000 or less, or your household total income $165,000 or less based on your <2020> notice of assessment(s) line 15000?': '' },
  ]);
  const handleCheckboxChange = (event, question, index) => {
    const { value } = event.target;
    console.log(question);
    console.log(value);
    console.log(index);
    console.log(answers);
    console.log(questions);
  };

  return (
    <div>
      <EligibilityPage
        year={year}
        questions={questions}
        setQuestions={setQuestions}
        handleCheckboxChange={handleCheckboxChange}
      />
    </div>
  );
};

export default ApplicationFormContainer;
