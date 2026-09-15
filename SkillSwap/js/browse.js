document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    document.getElementById('welcome-name').textContent = currentUser.name.split(' ')[0];

    // Populate dashboard stats
    document.getElementById('stat-offered').textContent = currentUser.canTeach ? currentUser.canTeach.length : 0;
    document.getElementById('stat-wanted').textContent = currentUser.wantsToLearn ? currentUser.wantsToLearn.length : 0;
    
    const requests = getRequests();
    const pendingCount = requests.filter(r => r.toUserId === currentUser.id && r.status === 'pending').length;
    document.getElementById('stat-pending').textContent = pendingCount;
    
    const connectionsCount = requests.filter(r => r.status === 'accepted' && (r.fromUserId === currentUser.id || r.toUserId === currentUser.id)).length;
    document.getElementById('stat-connections').textContent = connectionsCount;

    const searchInput = document.getElementById('search-input');
    const categoryFilter = document.getElementById('category-filter');
    const ratingFilter = document.getElementById('rating-filter');
    const usersGrid = document.getElementById('users-grid');

    const users = getUsers().filter(u => u.id !== currentUser.id); // Exclude current user

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
            const teachTags = user.canTeach.map(skill => `<span class="skill-tag">${skill}</span>`).join('');
            const learnTags = user.wantsToLearn.map(skill => `<span class="skill-tag want">${skill}</span>`).join('');
            
            card.innerHTML = `
                <div class="user-card-header">
                    <div class="avatar">${initials}</div>
                    <div class="user-info">
                        <h3>${user.name}</h3>
                        <p>📍 ${user.location}</p>
                        <div class="user-rating">⭐ ${user.rating.toFixed(1)} (${user.reviews ? user.reviews.length : 0} reviews)</div>
                    </div>
                </div>
                <div class="user-bio">${user.bio.length > 80 ? user.bio.substring(0, 80) + '...' : user.bio}</div>
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

    function filterUsers() {
        const query = searchInput.value.toLowerCase();
        const category = categoryFilter.value.toLowerCase();
        const minRating = parseFloat(ratingFilter.value) || 0;

        const filtered = users.filter(user => {
            // Search text
            const textMatch = 
                user.name.toLowerCase().includes(query) ||
                user.location.toLowerCase().includes(query) ||
                user.canTeach.some(s => s.toLowerCase().includes(query)) ||
                user.wantsToLearn.some(s => s.toLowerCase().includes(query));
            
            // Category filter
            let categoryMatch = true;
            if (category) {
                // simple mapping for demo
                const allSkills = [...user.canTeach, ...user.wantsToLearn].map(s => s.toLowerCase());
                if (category === 'programming') {
                    categoryMatch = allSkills.some(s => ['java', 'python', 'javascript', 'html', 'css', 'sql', 'machine learning', 'web development', 'spring boot'].includes(s));
                } else if (category === 'design') {
                    categoryMatch = allSkills.some(s => ['ui/ux', 'design', 'figma', 'photoshop'].includes(s));
                } else if (category === 'business') {
                    categoryMatch = allSkills.some(s => ['business', 'marketing', 'public speaking'].includes(s));
                } else if (category === 'music') {
                    categoryMatch = allSkills.some(s => ['guitar', 'music'].includes(s));
                } else if (category === 'languages') {
                    categoryMatch = allSkills.some(s => ['english', 'spanish', 'french'].includes(s));
                } else if (category === 'photography') {
                    categoryMatch = allSkills.some(s => ['photography', 'video editing'].includes(s));
                }
            }

            // Rating filter
            const ratingMatch = user.rating >= minRating;

            return textMatch && categoryMatch && ratingMatch;
        });

        renderUsers(filtered);
    }

    // Event listeners
    searchInput.addEventListener('input', filterUsers);
    categoryFilter.addEventListener('change', filterUsers);
    ratingFilter.addEventListener('change', filterUsers);

    window.resetFilters = function() {
        searchInput.value = '';
        categoryFilter.value = '';
        ratingFilter.value = '0';
        filterUsers();
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
        
        const targetUser = users.find(u => u.id === userId);
        document.getElementById('modal-teach-skills').textContent = targetUser.canTeach.join(', ');
        document.getElementById('modal-learn-skills').textContent = targetUser.wantsToLearn.join(', ');
        
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

    requestForm.addEventListener('submit', (e) => {
        e.preventDefault();
        const message = document.getElementById('request-message').value.trim();
        
        const requests = getRequests();
        
        // Check if already requested
        const exists = requests.find(r => r.fromUserId === currentUser.id && r.toUserId === currentTargetUserId && r.status === 'pending');
        
        if (exists) {
            showToast('You already have a pending request with this user.', 'error');
            closeModal();
            return;
        }

        const newRequest = {
            id: Date.now(),
            fromUserId: currentUser.id,
            toUserId: currentTargetUserId,
            message: message,
            status: 'pending',
            date: new Date().toISOString()
        };

        requests.push(newRequest);
        saveRequests(requests);
        
        showToast('Request sent successfully!');
        closeModal();
    });

    // Initial render
    renderUsers(users);
});
