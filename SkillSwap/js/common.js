// Common Utilities for SkillSwap

// --- Local Storage Helpers ---
function getUsers() {
  return JSON.parse(localStorage.getItem('users')) || [];
}

function saveUsers(users) {
  localStorage.setItem('users', JSON.stringify(users));
}

function getCurrentUser() {
  const user = localStorage.getItem('currentUser');
  return user ? JSON.parse(user) : null;
}

function setCurrentUser(user) {
  localStorage.setItem('currentUser', JSON.stringify(user));
}

function logout() {
  localStorage.removeItem('currentUser');
  window.location.href = 'index.html';
}

function getRequests() {
  return JSON.parse(localStorage.getItem('requests')) || [];
}

function saveRequests(requests) {
  localStorage.setItem('requests', JSON.stringify(requests));
}

function getMessages() {
  return JSON.parse(localStorage.getItem('messages')) || [];
}

function saveMessages(messages) {
  localStorage.setItem('messages', JSON.stringify(messages));
}

function getReviews() {
  return JSON.parse(localStorage.getItem('reviews')) || [];
}

function saveReviews(reviews) {
  localStorage.setItem('reviews', JSON.stringify(reviews));
}

// --- Auth Protection ---
function requireAuth() {
  if (!getCurrentUser()) {
    window.location.href = 'login.html';
  }
}

function redirectIfAuthenticated() {
  if (getCurrentUser()) {
    window.location.href = 'browse.html';
  }
}

// --- UI Helpers ---
function showToast(message, type = 'success') {
  const toastContainer = document.getElementById('toast-container') || createToastContainer();
  const toast = document.createElement('div');
  toast.className = `toast toast-${type}`;
  toast.innerText = message;
  
  toastContainer.appendChild(toast);
  
  // Show animation
  setTimeout(() => {
    toast.classList.add('show');
  }, 100);
  
  // Hide and remove
  setTimeout(() => {
    toast.classList.remove('show');
    setTimeout(() => {
      toast.remove();
    }, 300);
  }, 3000);
}

function createToastContainer() {
  const container = document.createElement('div');
  container.id = 'toast-container';
  document.body.appendChild(container);
  return container;
}

function setupNavbar() {
  const currentUser = getCurrentUser();
  const navContainer = document.getElementById('navbar-container');
  if (!navContainer) return;
  
  if (currentUser) {
    navContainer.innerHTML = `
      <nav class="navbar">
        <a href="browse.html" class="nav-logo">SkillSwap</a>
        <button class="nav-toggle" id="nav-toggle">☰</button>
        <ul class="nav-links" id="nav-links">
          <li><a href="browse.html">Browse Skills</a></li>
          <li><a href="requests.html">Requests</a></li>
          <li><a href="chat.html">Chat</a></li>
          <li><a href="nearby.html">Nearby</a></li>
          <li><a href="profile.html?id=${currentUser.id}">Profile</a></li>
          <li><button class="btn btn-secondary btn-sm" onclick="logout()">Logout</button></li>
        </ul>
      </nav>
    `;
  } else {
    navContainer.innerHTML = `
      <nav class="navbar">
        <a href="index.html" class="nav-logo">SkillSwap</a>
        <button class="nav-toggle" id="nav-toggle">☰</button>
        <ul class="nav-links" id="nav-links">
          <li><a href="index.html#how-it-works">How It Works</a></li>
          <li><a href="login.html" class="btn btn-secondary btn-sm">Login</a></li>
          <li><a href="register.html" class="btn btn-primary btn-sm">Sign Up</a></li>
        </ul>
      </nav>
    `;
  }
  
  const navToggle = document.getElementById('nav-toggle');
  const navLinks = document.getElementById('nav-links');
  
  if (navToggle && navLinks) {
    navToggle.addEventListener('click', () => {
      navLinks.classList.toggle('active');
    });
  }
}

// Generate initials for avatar
function getInitials(name) {
  return name.split(' ').map(n => n[0]).join('').substring(0, 2).toUpperCase();
}

// Ensure navbar is loaded
document.addEventListener('DOMContentLoaded', setupNavbar);
