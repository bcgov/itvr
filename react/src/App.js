import 'regenerator-runtime/runtime';

import axios from 'axios';
import React from 'react';
import { Switch } from 'react-router';
import { Route, BrowserRouter } from 'react-router-dom';

import settings from './app/settings';
import EligibilityPageContainer from './eligibility_page/EligibilityPageContainer';

const { API_BASE } = settings;
axios.defaults.withCredentials = true;
axios.defaults.baseURL = API_BASE;

const App = () => (
  <div className="App">
    <div className="App-body">
      <BrowserRouter>
        <Switch>
          <Route
            path="/"
            component={EligibilityPageContainer}
          />
        </Switch>
      </BrowserRouter>
    </div>
  </div>
);

export default App;
