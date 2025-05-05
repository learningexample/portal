import React from 'react';
import { Link, NavLink } from 'react-router-dom';
import './NavBar.css';

const NavBar = () => {
  return (
    <nav className="navbar">
      <div className="navbar-container">
        <div className="navbar-logo">
          <Link to="/">
            <img src="/assets/images/logo.svg" alt="AI Portal Logo" height="40" />
            <span>AI Portal</span>
          </Link>
        </div>
        <div className="navbar-links">
          <NavLink to="/" end>Dashboard</NavLink>
          <NavLink to="/app-store">App Store</NavLink>
          <NavLink to="/department-apps">Department Apps</NavLink>
        </div>
        <div className="navbar-user">
          <span>John Doe</span>
          <img src="/assets/images/user-avatar.svg" alt="User" className="avatar" />
        </div>
      </div>
    </nav>
  );
};

export default NavBar;