import React from 'react';
import { ToastContainer } from 'react-toastify';

import 'react-toastify/dist/ReactToastify.css';
// minified version is also included
// import 'react-toastify/dist/ReactToastify.min.css';

export default function Toast(){

  return (
    <div>
      <ToastContainer />
    </div>
  );
}