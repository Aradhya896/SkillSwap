import os

# LOGIN.HTML
login_path = "login.html"
with open(login_path, "r", encoding="utf-8") as f:
    login_html = f.read()

# Replace script part
new_login_script = """
    <script src="js/common.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            redirectIfAuthenticated();

            const loginForm = document.getElementById('login-form');
            
            loginForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const email = document.getElementById('email').value.trim();
                const password = document.getElementById('password').value;
                const emailError = document.getElementById('email-error');
                const passwordError = document.getElementById('password-error');
                
                emailError.classList.remove('active');
                passwordError.classList.remove('active');
                
                if (!email || !password) return;
                
                try {
                    const response = await fetchWithAuth('/auth/login', {
                        method: 'POST',
                        body: { email, password }
                    });
                    
                    // store token and user
                    const user = response.user;
                    user.token = response.token;
                    setCurrentUser(user);
                    
                    showToast('Login successful!');
                    setTimeout(() => {
                        window.location.href = 'browse.html';
                    }, 1000);
                } catch (error) {
                    showToast('Invalid email or password', 'error');
                    emailError.innerText = "Invalid credentials";
                    emailError.classList.add('active');
                }
            });
        });
    </script>
</body>
"""
login_html = login_html.replace("""
    <script src="js/data.js"></script>
    <script src="js/common.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            redirectIfAuthenticated();

            const loginForm = document.getElementById('login-form');
            
            loginForm.addEventListener('submit', (e) => {
                e.preventDefault();
                
                const email = document.getElementById('email').value.trim();
                const password = document.getElementById('password').value;
                const emailError = document.getElementById('email-error');
                const passwordError = document.getElementById('password-error');
                
                emailError.classList.remove('active');
                passwordError.classList.remove('active');
                
                if (!email) {
                    emailError.innerText = "Email is required";
                    emailError.classList.add('active');
                    return;
                }
                
                if (!password) {
                    passwordError.innerText = "Password is required";
                    passwordError.classList.add('active');
                    return;
                }
                
                const users = getUsers();
                const user = users.find(u => u.email === email && u.password === password);
                
                if (user) {
                    setCurrentUser(user);
                    showToast('Login successful!');
                    setTimeout(() => {
                        window.location.href = 'browse.html';
                    }, 1000);
                } else {
                    showToast('Invalid email or password', 'error');
                    emailError.innerText = "Invalid credentials";
                    emailError.classList.add('active');
                }
            });
        });
    </script>
</body>""", new_login_script)

with open(login_path, "w", encoding="utf-8") as f:
    f.write(login_html)


# REGISTER.HTML
register_path = "register.html"
with open(register_path, "r", encoding="utf-8") as f:
    register_html = f.read()

new_register_script = """
    <script src="js/common.js"></script>
    <script>
        document.addEventListener('DOMContentLoaded', () => {
            redirectIfAuthenticated();

            const registerForm = document.getElementById('register-form');
            
            registerForm.addEventListener('submit', async (e) => {
                e.preventDefault();
                
                const name = document.getElementById('name').value.trim();
                const email = document.getElementById('email').value.trim();
                const location = document.getElementById('location').value.trim();
                const password = document.getElementById('password').value;
                const confirmPassword = document.getElementById('confirm-password').value;
                const college = document.getElementById('college').value.trim();
                const canTeachRaw = document.getElementById('can-teach').value.trim();
                const wantsLearnRaw = document.getElementById('wants-learn').value.trim();
                const bio = document.getElementById('bio').value.trim();
                
                const formError = document.getElementById('form-error');
                formError.classList.remove('active');
                
                if (password.length < 6) {
                    formError.innerText = "Password must be at least 6 characters long.";
                    formError.classList.add('active');
                    return;
                }
                
                if (password !== confirmPassword) {
                    formError.innerText = "Passwords do not match.";
                    formError.classList.add('active');
                    return;
                }
                
                const canTeach = canTeachRaw.split(',').map(s => s.trim()).filter(s => s);
                const wantsToLearn = wantsLearnRaw.split(',').map(s => s.trim()).filter(s => s);
                
                if (canTeach.length === 0 || wantsToLearn.length === 0) {
                    formError.innerText = "Please list at least one skill for both teaching and learning.";
                    formError.classList.add('active');
                    return;
                }
                
                try {
                    const response = await fetchWithAuth('/auth/register', {
                        method: 'POST',
                        body: {
                            name, email, password, location, college, bio,
                            skillsToTeach: canTeach,
                            skillsToLearn: wantsToLearn
                        }
                    });
                    
                    showToast('Registration successful! Please login.');
                    setTimeout(() => {
                        window.location.href = 'login.html';
                    }, 1000);
                } catch (error) {
                    formError.innerText = "Registration failed. Email might be in use.";
                    formError.classList.add('active');
                }
            });
        });
    </script>
</body>
"""

import re
register_html = re.sub(r'    <script src="js/data\.js"></script>\s*<script src="js/common\.js"></script>.*?</body>', new_register_script, register_html, flags=re.DOTALL)

with open(register_path, "w", encoding="utf-8") as f:
    f.write(register_html)
