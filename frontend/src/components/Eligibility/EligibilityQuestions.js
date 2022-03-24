/* eslint-disable react/jsx-indent */
import React from 'react';
import Radio from '@mui/material/Radio';
import RadioGroup from '@mui/material/RadioGroup';
import FormControlLabel from '@mui/material/FormControlLabel';
import FormControl from '@mui/material/FormControl';
import FormLabel from '@mui/material/FormLabel';
import FormHelperText from '@mui/material/FormHelperText';
import { red } from '@mui/material/colors';

const EligibilityQuestions = (props) => {
  const { question, index, handleCheckboxChange } = props;
  return (
    <div key={index}>
      <FormControl>
        <FormLabel className="label" id="demo-radio-buttons-group-label">
          {question.question}
        </FormLabel>
        <RadioGroup
          aria-labelledby="demo-radio-buttons-group-label"
          name="radio-buttons-group"
          onChange={(e) => handleCheckboxChange(e, index)}
        >
          <FormControlLabel value="yes" control={<Radio />} label="Yes" />
          <FormControlLabel value="no" control={<Radio />} label="No" />
        </RadioGroup>
        <FormHelperText
          sx={{
            color: red[800]
          }}
        >
          {question.showError && question.errorMessage}
        </FormHelperText>
      </FormControl>
    </div>
  );
};

export default EligibilityQuestions;
