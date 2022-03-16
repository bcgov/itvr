import React from "react";

const Header = (props) => {
  const { pageTitle } = props;
  return (
    <div className="page-header">
      <div className="cleanbc-banner">
        <a
          href="http://www.gov.bc.ca"
          rel="noopener noreferrer"
          target="_blank"
        >
          <img src="../../BCID_H_rgb_rev.png" alt="Government of B.C." />
        </a>
        <span>CleanBC | Go Electric BC</span>
      </div>
      <div className="title">
        <h1>Electric Vehicle Rebates</h1>
        <h2>for Individuals and Households</h2>
      </div>
    </div>
  );
};
export default Header;
