import React, { useCallback, useEffect } from 'react';
import { useDropzone } from 'react-dropzone';
import { useFormContext } from 'react-hook-form';
import Box from '@mui/material/Box';
import Button from '@mui/material/Button';
import DeleteIcon from '@mui/icons-material/Delete';
import UploadIcon from '@mui/icons-material/Upload';

const MAX_SIZE = 5242880; //5MB in bytes
const getFileSize = (bytes) => {
  if (bytes === 0) {
    return '0 bytes';
  }

  const sizes = ['bytes', 'KB', 'MB', 'GB', 'TB'];
  let i = Math.min(Math.floor(Math.log(bytes) / Math.log(1024)), 4);
  const filesize = parseFloat((bytes / 1000 ** i).toFixed(1));

  return `${filesize} ${sizes[i]}`;
};

const fileTooLarge = (bytes, maxBytes) => {
  if (bytes <= maxBytes) {
    return false;
  }
  return true;
};

const FileDropArea = ({
  name = 'documents',
  accept = 'image/png, image/jpg, image/jpeg'
}) => {
  const { register, unregister, setValue, watch } = useFormContext();
  const files = watch(name);
  const onDrop = useCallback(
    (droppedFiles) => {
      const newFiles =
        (files && [...files].concat(droppedFiles)) || droppedFiles;
      setValue(name, newFiles);
    },
    [setValue, name, files]
  );
  const { getRootProps, getInputProps } = useDropzone({
    onDrop,
    accept
  });
  useEffect(() => {
    register(name, {
      validate: {
        twoOrMore: (inputtedFiles) => {
          if (!inputtedFiles || inputtedFiles.length < 2) {
            return false;
          }
          return true;
        },
        maxSize: (inputtedFiles) => {
          for (const i in inputtedFiles) {
            const inputtedFile = inputtedFiles[i];
            const inputtedFileSize = inputtedFile.size;
            if (fileTooLarge(inputtedFileSize, MAX_SIZE)) {
              return false;
            }
          }
          return true;
        }
      }
    });
    return () => {
      unregister(name);
    };
  }, [register, unregister, name]);

  const removeFile = (removedFile) => {
    const found = files.findIndex((file) => file === removedFile);
    files.splice(found, 1);
    setValue(name, files);
  };

  return (
    <div className="bordered">
      <div>
        <div className="content">
          <Box p={3}>
            <div {...getRootProps()} aria-label="File Upload" id={name}>
              <input name={name} {...getInputProps()} />
              <div className="file-upload">
                <UploadIcon />
                <br />
                <label htmlFor={name}>Drag and Drop files here</label> or <br />
                <Box p={2}>
                  <Button variant="outlined">
                    browse to select a file from your machine to upload.
                  </Button>
                </Box>
              </div>
            </div>
          </Box>
        </div>
        {files && files.length > 0 && (
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
