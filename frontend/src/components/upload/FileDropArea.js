import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import Grid from '@mui/material/Grid';
import DeleteIcon from '@mui/icons-material/Delete';
import UploadIcon from '@mui/icons-material/Upload';

const getFileSize = (bytes) => {
  if (bytes === 0) {
    return '0 bytes';
  }

  const k = 1024;
  const sizes = ['bytes', 'KB', 'MB', 'GB', 'TB'];
  let i = Math.min(Math.floor(Math.log(bytes) / Math.log(k)), 4);
  const filesize = parseFloat((bytes / k ** i).toFixed(1));

  return `${filesize} ${sizes[i]}`;
};

const FormRow = ({ file, removeFile }) => {
  const { name, size } = file;
  return (
    <React.Fragment key={name}>
      <Grid item xs={7}>
        {name}
      </Grid>
      <Grid item xs={3} className="upload-row">
        {getFileSize(size)}
      </Grid>
      <Grid item xs={2} className="upload-row">
        <Button
          className="delete"
          onClick={() => {
            removeFile(file);
          }}
          type="button"
          id="trash-button"
        >
          <DeleteIcon />
        </Button>
      </Grid>
    </React.Fragment>
  );
};

const FileDropArea = () => {
  const [files, setFiles] = useState([]);
  const [dropMessage, setDropMessage] = useState('');
  const onDrop = useCallback(
    (acceptedFiles) => {
      setDropMessage('');
      setFiles([...files, ...acceptedFiles]);
    },
    [files]
  );

  const { getRootProps, getInputProps } = useDropzone({ onDrop });

  const removeFile = (removedFile) => {
    const found = files.findIndex((file) => file === removedFile);
    files.splice(found, 1);
  };

  return (
    <div className="bordered">
      <div>
        <div className="content">
          <Box p={3}>
            <div {...getRootProps()}>
              <input {...getInputProps()} />
              <div className="file-upload">
                <UploadIcon />
                <br />
                Drag and Drop files here or <br />
                <Box p={2}>
                  <Button variant="outlined">
                    browse to select a file from your machine to upload.
                  </Button>
                </Box>
                {dropMessage && <div>{dropMessage}</div>}
              </div>
            </div>
          </Box>
        </div>
        {files.length > 0 && (
          <Box className="upload-list" pt={3} rb={2}>
            <Grid container direction="row">
              <Grid item xs={7}>
                Filename
              </Grid>
              <Grid item xs={3}>
                Size
              </Grid>
              <Grid item xs={2} />
              {files.map((file) => (
                <FormRow file={file} removeFile={removeFile}></FormRow>
              ))}
            </Grid>
          </Box>
        )}
      </div>
    </div>
  );
};

export default FileDropArea;
