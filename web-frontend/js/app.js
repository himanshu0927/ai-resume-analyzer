document.addEventListener('DOMContentLoaded', () => {
  renderNavbar();
});

function renderNavbar() {
  const userJson = localStorage.getItem('user');
  const user = userJson ? JSON.parse(userJson) : null;
  const navContainer = document.getElementById('navbar-container');

  if (!navContainer) return;

  const currentPath = window.location.pathname.split('/').pop() || 'index.html';

  if (user) {
    navContainer.innerHTML = `
      <header class="navbar">
        <a href="dashboard.html" class="logo-brand">
          <div class="logo-icon">AI</div>
          <span>Resume Analyzer</span>
        </a>
        <ul class="nav-links">
          <li><a href="dashboard.html" class="${currentPath === 'dashboard.html' ? 'active' : ''}">Dashboard</a></li>
          <li><a href="analyzer.html" class="${currentPath === 'analyzer.html' ? 'active' : ''}">Resume Analyzer</a></li>
          <li><a href="job-matcher.html" class="${currentPath === 'job-matcher.html' ? 'active' : ''}">Job Matcher</a></li>
          <li><a href="skill-gap.html" class="${currentPath === 'skill-gap.html' ? 'active' : ''}">Skill Gap</a></li>
          <li><a href="recommendations.html" class="${currentPath === 'recommendations.html' ? 'active' : ''}">Recommendations</a></li>
          <li><a href="history.html" class="${currentPath === 'history.html' ? 'active' : ''}">My Analyses</a></li>
          <li><a href="profile.html" class="${currentPath === 'profile.html' ? 'active' : ''}">Profile</a></li>
          <li><button onclick="handleLogout()" class="btn-btn btn-outline" style="padding: 0.4rem 0.8rem; font-size: 0.8rem;">Logout</button></li>
        </ul>
      </header>
    `;
  } else {
    navContainer.innerHTML = `
      <header class="navbar">
        <a href="index.html" class="logo-brand">
          <div class="logo-icon">AI</div>
          <span>Resume Analyzer</span>
        </a>
        <ul class="nav-links">
          <li><a href="index.html" class="${currentPath === 'index.html' ? 'active' : ''}">Home</a></li>
          <li><a href="login.html" class="btn-btn btn-outline">Sign In</a></li>
          <li><a href="register.html" class="btn-btn btn-primary">Get Started</a></li>
        </ul>
      </header>
    `;
  }
}

function handleLogout() {
  localStorage.removeItem('token');
  localStorage.removeItem('user');
  window.location.href = 'login.html';
}

function checkAuthProtection() {
  const token = localStorage.getItem('token');
  if (!token) {
    window.location.href = 'login.html';
  }
}
