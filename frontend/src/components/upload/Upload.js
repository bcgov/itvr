import React from 'react';
import Box from '@mui/material/Box';
import FileDropArea from './FileDropArea';

const Upload = (props) => {
  const { errors, applicationType } = props;
  return (
    <>
      <Box className="form-upload-instructions">
        <h3>Upload images of your ID</h3>
        <h5>Take a picture of:</h5>
        <ul>
          <li>
            The photo side of your BC Driver's Licence{' '}
            {applicationType === 'spouse' && ' or BC Services Card'}
          </li>
          <li>
            A secondary piece of ID like a financial statement or utility bill
            that has been issued in the last 90 days
          </li>
        </ul>
        <p>
          Both pieces of ID must show the same address. Image files must be in
          jpg or png format.
        </p>
        <p>
          <a href="/identificationExamples" target="_blank">
          See examples of accepted ID 
          </a>
         (Note: Link opens in a new tab to prevent losing form data)
        </p>
      </Box>
      {errors?.documents?.type === 'exactlyTwo' && (
        <p className="error">Need exactly 2 files</p>
      )}
      {errors?.documents?.type === 'maxSize' && (
        <p className="error">No file may exceed 5MB</p>
      )}
      <FileDropArea name="documents" />
    </>
  );
};
export default Upload;
