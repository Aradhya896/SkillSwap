document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    
    document.getElementById('password-form').addEventListener('submit', (e) => {
        e.preventDefault();
        
        const current = document.getElementById('current-password').value;
        const newPass = document.getElementById('new-password').value;
        const confirmPass = document.getElementById('confirm-password').value;
        
        if (current !== currentUser.password) {
            showToast('Current password is incorrect', 'error');
            return;
        }
        
        if (newPass.length < 6) {
            showToast('New password must be at least 6 characters', 'error');
            return;
        }
        
        if (newPass !== confirmPass) {
            showToast('New passwords do not match', 'error');
            return;
        }
        
        // Update password
        const users = getUsers();
        const userIndex = users.findIndex(u => u.id === currentUser.id);
        
        users[userIndex].password = newPass;
        saveUsers(users);
        
        currentUser.password = newPass;
        setCurrentUser(currentUser);
        
        showToast('Password updated successfully!');
        e.target.reset();
    });

    window.deleteAccount = function() {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            const users = getUsers();
            const filteredUsers = users.filter(u => u.id !== currentUser.id);
            saveUsers(filteredUsers);
            
            logout();
        }
    };
});
