import React, { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import UploadIcon from '@mui/icons-material/Upload';

const getFileSize = (bytes) => {
  if (bytes === 0) {
    return '0 bytes';
  }

  const sizes = ['bytes', 'KB', 'MB', 'GB', 'TB'];
  let i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), 4);
  const filesize = parseFloat((bytes / 1000 ** i).toFixed(1));

  return `${filesize} ${sizes[i]}`;
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
    setFiles([...files]);
  };

  return (
    <div className="bordered">
      <div>
        <div className="content">
          <Box p={3}>
            <div {...getRootProps()}>
              <input {...getInputProps()} id="documents" />
              <div className="file-upload">
                <UploadIcon />
                <br />
                <label htmlFor="documents">
                  Drag and Drop files here
                </label> or <br />
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
            <table aria-label="Uploaded Files List" className="document-table">
              <thead>
                <tr>
                  <th style={{ textAlign: 'left' }}>Filename</th>
                  <th style={{ textAlign: 'left' }}>Size</th>
                  <th style={{ textAlign: 'left' }}>Virus Scan</th>
                  <th></th>
                </tr>
              </thead>
              <tbody>
                {files.map((file) => (
                  <tr key={file.name} className="upload-row">
                    <td>{file.name}</td>
                    <td style={{ textAlign: 'right' }}>
                      {getFileSize(file.size)}
                    </td>
                    <td></td>
                    <td style={{ textAlign: 'right' }}>
                      <Button
                        className="delete"
                        onClick={() => {
                          removeFile(file);
                        }}
                        type="button"
                      >
                        <DeleteIcon sx={{ color: 'red' }} />
                      </Button>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </Box>
        )}
      </div>
    </div>
  );
};

export default FileDropArea;
