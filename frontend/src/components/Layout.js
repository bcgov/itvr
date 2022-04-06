import React from 'react';
import Header from './Header';

const Layout = ({ children }) => {
  return (
    <>
      <Header />
      <main className="page-content">{children}</main>
    </>
  );
};
export default Layout;
