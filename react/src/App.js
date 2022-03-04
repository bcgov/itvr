import 'regenerator-runtime/runtime';

import axios from 'axios';
import React from 'react';
import { Switch } from 'react-router';
import { Route, BrowserRouter } from 'react-router-dom';

import settings from './app/settings';
import ApplicationFormContainer from './rebate_application_form/ApplicationFormContainer';
import Main from './Main';

const { API_BASE } = settings;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = API_BASE;

const App = () => (
  <div className="App">
    <header className="App-header">
      <div className="container">
        <a href="http://www.gov.bc.ca">
          <div className="brand-logo" />
        </a>
        <h1>
          Income Tested Verified Rebates
        </h1>
      </div>
    </header>

    <div className="App-body">
      <BrowserRouter>
        <Switch>
          <Route
            path="/"
            component={Main}
          />
          <Route
            path="/form"
            component={ApplicationFormContainer}
          />
        </Switch>
      </BrowserRouter>
    </div>
  </div>
);

export default App;
