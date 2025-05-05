import { Component } from '@angular/core';

@Component({
  selector: 'app-navbar',
  template: `
    <nav class="navbar">
      <div class="navbar-container">
        <div class="navbar-logo">
          <a routerLink="/">
            <img src="/assets/images/logo.svg" alt="AI Portal Logo" height="40">
            <span>AI Portal</span>
          </a>
        </div>
        <div class="navbar-links">
          <a routerLink="/" routerLinkActive="active" [routerLinkActiveOptions]="{exact: true}">Dashboard</a>
          <a routerLink="/app-store" routerLinkActive="active">App Store</a>
          <a routerLink="/department-apps" routerLinkActive="active">Department Apps</a>
        </div>
        <div class="navbar-user">
          <span>John Doe</span>
          <img src="/assets/images/user-avatar.svg" alt="User" class="avatar">
        </div>
      </div>
    </nav>
  `,
  styles: [`
    .navbar {
      background-color: #2c3e50;
      color: white;
      padding: 12px 0;
    }
    .navbar-container {
      display: flex;
      align-items: center;
      justify-content: space-between;
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
    }
    .navbar-logo a {
      display: flex;
      align-items: center;
      color: white;
      text-decoration: none;
      font-weight: bold;
      font-size: 1.3rem;
    }
    .navbar-logo img {
      margin-right: 10px;
    }
    .navbar-links {
      display: flex;
      gap: 20px;
    }
    .navbar-links a {
      color: white;
      text-decoration: none;
      padding: 5px 10px;
      border-radius: 4px;
      transition: background-color 0.3s;
    }
    .navbar-links a:hover, .navbar-links a.active {
      background-color: rgba(255, 255, 255, 0.2);
    }
    .navbar-user {
      display: flex;
      align-items: center;
      gap: 10px;
    }
    .avatar {
      width: 32px;
      height: 32px;
      border-radius: 50%;
    }
  `]
})
export class NavbarComponent {}