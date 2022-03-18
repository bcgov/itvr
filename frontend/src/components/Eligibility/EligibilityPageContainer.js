import React, { useState } from 'react';
import EligibilityPage from './EligibilityPage';

const ApplicationFormContainer = () => {
  const [loading, setLoading] = useState(false);
  const [details, setDetails] = useState({});
  const date = new Date();
  // get the date as a string
  const month = date.getMonth();
  let taxYear = date.getFullYear();
  if (month < 6) {
    // if its earlier than July 1
    // jan = 0, feb = 1, mar = 2, apr = 3, may = 4, june = 5, july = 6
    taxYear -= 2;
  } else {
    // if its july or later
    taxYear -= 1;
  }
  const [questions, setQuestions] = useState([
    {
      question:
        'Have you previously received an electric vehicle rebate from the Government of British Columbia?',
      answer: '',
      expectedAnswer: 'no',
      errorMessage: 'Sorry you are not eligible to claim a second rebate.',
      showError: false
    },
    {
      question:
        'Do you reside in British Columbia and have a valid B.C. Drivers Licence?',
      answer: '',
      expectedAnswer: 'yes',
      errorMessage: `Sorry you are not eligible to claim a rebate without a B.C. address and driver's licence.`,
      showError: false
    },
    {
      question:
        'Did you file a year tax return with the Canada Revenue Agency (CRA)?',
      answer: '',
      expectedAnswer: 'yes',
      errorMessage: `Sorry you are not eligible to claim a rebate without having filed a ${taxYear} tax return with the CRA.`,
      showError: false
    },
    {
      question: `Was your individual total income $100,000 or less, or your household total 
    income $165,000 or less based on your ${taxYear} notice of assessment(s) line 15000?`,
      answer: '',
      expectedAnswer: 'yes',
      errorMessage: 'Sorry you are not eligible to claim a rebate.',
      showError: false
    }
  ]);
  const [eligible, setEligible] = useState(false);

  const handleCheckboxChange = (event, index) => {
    const { value } = event.target;
    let answers = [...questions];
    answers[index].answer = value;
    if (questions[index].answer !== questions[index].expectedAnswer) {
      answers[index].showError = true;
    } else {
      answers[index].showError = false;
    }
    setQuestions(answers);
    let correctAnswers = 0;
    questions.forEach((q) => {
      if (q.answer === q.expectedAnswer) {
        correctAnswers += 1;
      } else {
        correctAnswers -= 1;
      }
    });
    if (correctAnswers === 4) {
      setEligible(true);
    } else {
      setEligible(false);
    }
  };

  return (
    <div>
      <EligibilityPage
        taxYear={taxYear}
        questions={questions}
        setQuestions={setQuestions}
        handleCheckboxChange={handleCheckboxChange}
        eligible={eligible}
      />
    </div>
  );
};

export default ApplicationFormContainer;
