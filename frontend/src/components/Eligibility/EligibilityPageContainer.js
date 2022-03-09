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
    year -= 2;
  } else {
    // if its july or later
    year -= 1;
  }
  const [questions, setQuestions] = useState([
    {
      question:
        'Have you previously received an electric vehicle rebate from the Government of British Columbia?',
      answer: '',
      expectedAnswer: 'no'
    },
    {
      question:
        'Do you reside in British Columbia and have a valid B.C. Drivers Licence?',
      answer: '',
      expectedAnswer: 'yes'
    },
    {
      question:
        'Did you file a year tax return with the Canada Revenue Agency (CRA)?',
      answer: '',
      expectedAnswer: 'yes'
    },
    {
      question: `Was your individual total income $100,000 or less, or your household total 
    income $165,000 or less based on your ${year} notice of assessment(s) line 15000?`,
      answer: '',
      expectedAnswer: 'yes'
    }
  ]);
  const [eligible, setEligible] = useState(false);

  const handleCheckboxChange = (event, question, index) => {
    const { value } = event.target;
    let answers = [...questions];
    answers[index].answer = value;
    setQuestions(answers);
    let correctAnswers = 0;
    questions.forEach((question) => {
      if (question.answer === question.expectedAnswer) {
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
        year={year}
        questions={questions}
        setQuestions={setQuestions}
        handleCheckboxChange={handleCheckboxChange}
        eligible={eligible}
      />
    </div>
  );
};

export default ApplicationFormContainer;
