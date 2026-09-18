import os

# BROWSE.JS
browse_js = """document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const currentUser = getCurrentUser();
    document.getElementById('welcome-name').textContent = currentUser.name.split(' ')[0];

    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const ratingFilter = document.getElementById('rating-filter');
    const usersGrid = document.getElementById('users-grid');

    let allUsers = [];

    // Load initial stats
    async function loadStats() {
        try {
            const me = await fetchWithAuth('/users/me');
            document.getElementById('stat-offered').textContent = me.skillsToTeach ? me.skillsToTeach.length : 0;
            document.getElementById('stat-wanted').textContent = me.skillsToLearn ? me.skillsToLearn.length : 0;
            
            const incoming = await fetchWithAuth('/requests/incoming');
            const sent = await fetchWithAuth('/requests/sent');
            const pendingCount = incoming.filter(r => r.status === 'pending').length;
            document.getElementById('stat-pending').textContent = pendingCount;
            
            const connectionsCount = incoming.filter(r => r.status === 'accepted').length + 
                                     sent.filter(r => r.status === 'accepted').length;
            document.getElementById('stat-connections').textContent = connectionsCount;
        } catch (err) {
            console.error('Error loading stats', err);
        }
    }

    async function loadUsers(search = '', location = '', minRating = 0) {
        try {
            let url = '/users?';
            if (search) url += `search=${encodeURIComponent(search)}&`;
            if (location) url += `location=${encodeURIComponent(location)}&`;
            if (minRating > 0) url += `minRating=${minRating}`;
            
            allUsers = await fetchWithAuth(url);
            // Filter out current user
            allUsers = allUsers.filter(u => u.id !== currentUser.id);
            renderUsers(allUsers);
        } catch (err) {
            console.error('Error loading users', err);
            usersGrid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">Unable to connect to server. Please try again.</div>`;
        }
    }

    function renderUsers(usersToRender) {
        usersGrid.innerHTML = '';

        if (usersToRender.length === 0) {
            usersGrid.innerHTML = `
                <div class="empty-state" style="grid-column: 1 / -1;">
                    <h2>No skill partners found</h2>
                    <p>Try searching for another skill or changing your filters.</p>
                    <button class="btn btn-secondary mt-2" onclick="resetFilters()">Clear Filters</button>
                </div>
            `;
            return;
        }

        usersToRender.forEach(user => {
            const card = document.createElement('div');
            card.className = 'card user-card';
            
            const initials = getInitials(user.name);
            const teachTags = (user.skillsToTeach || []).map(skill => `<span class="skill-tag">${skill}</span>`).join('');
            const learnTags = (user.skillsToLearn || []).map(skill => `<span class="skill-tag want">${skill}</span>`).join('');
            
            card.innerHTML = `
                <div class="user-card-header">
                    <div class="avatar">${initials}</div>
                    <div class="user-info">
                        <h3>${user.name}</h3>
                        <p>📍 ${user.location || 'Unknown'}</p>
                        <div class="user-rating">⭐ ${user.rating ? user.rating.toFixed(1) : '0.0'} (${user.reviewCount || 0} reviews)</div>
                    </div>
                </div>
                <div class="user-bio">${(user.bio || '').length > 80 ? user.bio.substring(0, 80) + '...' : user.bio}</div>
                <div class="skills-section">
                    <h4>Can Teach</h4>
                    <div class="skills-list">${teachTags}</div>
                </div>
                <div class="skills-section">
                    <h4>Wants to Learn</h4>
                    <div class="skills-list">${learnTags}</div>
                </div>
                <div class="card-actions">
                    <a href="profile.html?id=${user.id}" class="btn btn-secondary btn-sm">View Profile</a>
                    <button onclick="openRequestModal(${user.id}, '${user.name.replace(/'/g, "\\'")}')" class="btn btn-primary btn-sm">Request</button>
                </div>
            `;
            usersGrid.appendChild(card);
        });
    }

    function handleFilter() {
        const query = searchInput.value.trim();
        const minRating = parseFloat(ratingFilter.value) || 0;
        
        // Backend search
        loadUsers(query, null, minRating);
    }

    // Event listeners
    let debounceTimer;
    searchInput.addEventListener('input', () => {
        clearTimeout(debounceTimer);
        debounceTimer = setTimeout(handleFilter, 300);
    });
    categoryFilter.addEventListener('change', () => {
        const cat = categoryFilter.value;
        if (cat) {
            searchInput.value = cat; // simple category search logic
        } else {
            searchInput.value = '';
        }
        handleFilter();
    });
    ratingFilter.addEventListener('change', handleFilter);

    window.resetFilters = function() {
        searchInput.value = '';
        categoryFilter.value = '';
        ratingFilter.value = '0';
        handleFilter();
    };

    // Modal Logic
    const modal = document.getElementById('request-modal');
    const closeBtn = modal.querySelector('.close-modal');
    const cancelBtn = document.getElementById('cancel-request');
    const requestForm = document.getElementById('exchange-form');
    let currentTargetUserId = null;

    window.openRequestModal = function(userId, userName) {
        currentTargetUserId = userId;
        document.getElementById('modal-user-name').textContent = userName;
        
        const targetUser = allUsers.find(u => u.id === userId);
        document.getElementById('modal-teach-skills').textContent = (targetUser.skillsToTeach || []).join(', ');
        document.getElementById('modal-learn-skills').textContent = (targetUser.skillsToLearn || []).join(', ');
        
        document.getElementById('request-message').value = '';
        modal.classList.add('active');
    };

    function closeModal() {
        modal.classList.remove('active');
        currentTargetUserId = null;
    }

    closeBtn.addEventListener('click', closeModal);
    cancelBtn.addEventListener('click', closeModal);
    
    // Close on outside click
    modal.addEventListener('click', (e) => {
        if (e.target === modal) closeModal();
    });

    // Close on escape
    document.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && modal.classList.contains('active')) closeModal();
    });

    requestForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        const message = document.getElementById('request-message').value.trim();
        
        try {
            await fetchWithAuth('/requests', {
                method: 'POST',
                body: { toUserId: currentTargetUserId, message }
            });
            showToast('Request sent successfully!');
            closeModal();
            loadStats();
        } catch (err) {
            showToast(err.message || 'Unable to send request.', 'error');
            closeModal();
        }
    });

    // Initial render
    loadStats();
    loadUsers();
});
"""

with open("js/browse.js", "w", encoding="utf-8") as f:
    f.write(browse_js)
