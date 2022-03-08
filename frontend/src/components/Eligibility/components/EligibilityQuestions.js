/* eslint-disable react/jsx-indent */
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';

const EligibilityQuestions = (props) => {
  const {
    question, index, setQuestions, handleCheckboxChange,
  } = props;
  return (
    <div key={index}>
      <FormControl>
        <FormLabel className="label" id="demo-radio-buttons-group-label">{Object.keys(question)[0]}</FormLabel>
        <RadioGroup
          aria-labelledby="demo-radio-buttons-group-label"
          name="radio-buttons-group"
          onChange={(e) => handleCheckboxChange(e, question, index)}
        >
          <FormControlLabel value="yes" control={<Radio />} label="Yes" />
          <FormControlLabel value="no" control={<Radio />} label="No" />
        </RadioGroup>
      </FormControl>
    </div>
  );
};

export default EligibilityQuestions;
