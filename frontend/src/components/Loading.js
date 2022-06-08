import React from 'react';
import { Backdrop, CircularProgress, Modal } from '@mui/material';

const Loading = ({ open = false }) => {
  return (
    <Modal open={open}>
      <Backdrop open={true} invisible={true}>
        <CircularProgress />
      </Backdrop>
    </Modal>
  );
};

export default Loading;
