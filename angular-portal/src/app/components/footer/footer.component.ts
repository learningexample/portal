import { Component } from '@angular/core';

@Component({
  selector: 'app-footer',
  template: `
    <footer class="footer">
      <div class="footer-container">
        <div class="footer-copyright">
          © 2025 AI Portal. All rights reserved.
        </div>
        <div class="footer-links">
          <a href="#">Privacy Policy</a>
          <a href="#">Terms of Service</a>
          <a href="#">Contact Us</a>
        </div>
      </div>
    </footer>
  `,
  styles: [`
    .footer {
      background-color: #2c3e50;
      color: white;
      padding: 20px 0;
      margin-top: 40px;
    }
    .footer-container {
      display: flex;
      justify-content: space-between;
      align-items: center;
      max-width: 1200px;
      margin: 0 auto;
      padding: 0 20px;
    }
    .footer-links {
      display: flex;
      gap: 20px;
    }
    .footer-links a {
      color: #ecf0f1;
      text-decoration: none;
      font-size: 0.9rem;
    }
    .footer-links a:hover {
      text-decoration: underline;
    }
  `]
})
export class FooterComponent {}