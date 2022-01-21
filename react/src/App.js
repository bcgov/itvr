import 'regenerator-runtime/runtime';

import axios from 'axios';
import React from 'react';
import { Switch } from 'react-router';
import { Route, BrowserRouter } from 'react-router-dom';

import settings from './app/settings';
import ApplicationFormContainer from './rebate_application_form/ApplicationFormContainer';

const { API_BASE } = settings;

axios.defaults.baseURL = API_BASE;

const App = () => (
  <div className="App">
    <header className="App-header">
      <div className="container">
        <a href="/">
          <div className="logo" />
        </a>
      </div>
    </header>

    <div className="App-body">
      <BrowserRouter>
        <Switch>
          <Route
            path="/"
            component={ApplicationFormContainer}
          />
        </Switch>
      </BrowserRouter>
    </div>
  </div>
);

export default App;
