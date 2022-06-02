import React from 'react';
import logo from '../styles/images/BCID_H_rgb_rev.png';

const Header = (props) => {
  return (
    <div className="page-header">
      <div className="cleanbc-banner">
        <a
          href="http://www.gov.bc.ca"
          rel="noopener noreferrer"
          target="_blank"
        >
          <img src={logo} alt="Government of B.C." />
        </a>
        <span>CleanBC Go Electric</span>
      </div>
      <div className="title">
        <h1>Passenger vehicle rebates</h1>
      </div>
    </div>
  );
};
export default Header;
