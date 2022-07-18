import React from 'react';
import logo from '../styles/images/BCID_H_rgb_rev.png';
import Logout from './Logout';

const Header = ({ logoutUri }) => {
  return (
    <div className="page-header">
      <div className="cleanbc-banner">
        <div className="left">
          <a href="http://www.gov.bc.ca" rel="noopener noreferrer">
            <img src={logo} alt="Government of B.C." />
          </a>
          <a href="https://goelectricbc.gov.bc.ca/" rel="noopener noreferrer">
            CleanBC Go Electric
          </a>
        </div>
        <div className="right">
          <Logout logoutUri={logoutUri} />
        </div>
      </div>
      <div className="title">
        <h1>Passenger vehicle rebates</h1>
      </div>
    </div>
  );
};
export default Header;
