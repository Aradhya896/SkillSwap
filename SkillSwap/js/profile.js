document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const urlParams = new URLSearchParams(window.location.search);
    const profileId = parseInt(urlParams.get('id'));

    // If no ID is provided, default to current user
    const targetUserId = profileId || currentUser.id;
    const users = getUsers();
    const profileUser = users.find(u => u.id === targetUserId);

    if (!profileUser) {
        document.querySelector('.profile-container').innerHTML = `
            <div class="empty-state">
                <h2>User not found</h2>
                <p>The user you are looking for does not exist.</p>
                <a href="browse.html" class="btn btn-primary mt-2">Back to Browse</a>
            </div>
        `;
        return;
    }

    const isOwnProfile = profileUser.id === currentUser.id;

    // Render Profile Data
    document.title = `${profileUser.name} - SkillSwap`;
    document.getElementById('profile-avatar').textContent = getInitials(profileUser.name);
    document.getElementById('profile-name').textContent = profileUser.name;
    document.getElementById('profile-location').textContent = `📍 ${profileUser.location}`;
    document.getElementById('profile-college').textContent = `🎓 ${profileUser.college || 'Not specified'}`;
    document.getElementById('profile-availability').textContent = `⏰ ${profileUser.availability || 'Flexible'}`;
    document.getElementById('profile-joined').textContent = `📅 Member`;
    
    document.getElementById('stat-rating').textContent = `${profileUser.rating.toFixed(1)}/5.0`;
    document.getElementById('stat-reviews').textContent = profileUser.reviews ? profileUser.reviews.length : 0;
    
    document.getElementById('profile-bio').textContent = profileUser.bio;

    // Render Skills
    const teachContainer = document.getElementById('skills-teach');
    teachContainer.innerHTML = profileUser.canTeach.map(s => `<span class="skill-tag">${s}</span>`).join('');

    const learnContainer = document.getElementById('skills-learn');
    learnContainer.innerHTML = profileUser.wantsToLearn.map(s => `<span class="skill-tag want">${s}</span>`).join('');

    // Actions
    const actionsContainer = document.getElementById('profile-actions');
    if (isOwnProfile) {
        actionsContainer.innerHTML = `
            <button class="btn btn-secondary" onclick="openEditModal()">Edit Profile</button>
        `;
    } else {
        actionsContainer.innerHTML = `
            <button class="btn btn-primary" onclick="openRequestModal()">Request Exchange</button>
            <button class="btn btn-secondary" onclick="messageUser()">Message</button>
        `;
    }

    // Reviews (dummy logic for now, we'll populate if they have real reviews from localstorage)
    const reviewsContainer = document.getElementById('profile-reviews');
    const allReviews = getReviews().filter(r => r.toUserId === targetUserId);
    
    if (allReviews.length === 0) {
        reviewsContainer.innerHTML = `<p class="text-muted">No reviews yet.</p>`;
    } else {
        reviewsContainer.innerHTML = allReviews.map(r => `
            <div class="review-card">
                <div class="review-header">
                    <span class="review-author">${r.authorName}</span>
                    <span class="review-stars">${'⭐'.repeat(r.rating)}</span>
                </div>
                <div class="review-text">${r.text}</div>
            </div>
        `).join('');
    }

    // Modals
    const editModal = document.getElementById('edit-modal');
    const requestModal = document.getElementById('request-modal');
    
    window.openEditModal = function() {
        document.getElementById('edit-name').value = profileUser.name;
        document.getElementById('edit-location').value = profileUser.location;
        document.getElementById('edit-college').value = profileUser.college;
        document.getElementById('edit-bio').value = profileUser.bio;
        document.getElementById('edit-teach').value = profileUser.canTeach.join(', ');
        document.getElementById('edit-learn').value = profileUser.wantsToLearn.join(', ');
        document.getElementById('edit-availability').value = profileUser.availability || '';
        editModal.classList.add('active');
    };

    window.openRequestModal = function() {
        document.getElementById('modal-user-name').textContent = profileUser.name;
        document.getElementById('modal-teach-skills').textContent = profileUser.canTeach.join(', ');
        document.getElementById('modal-learn-skills').textContent = profileUser.wantsToLearn.join(', ');
        document.getElementById('request-message').value = '';
        requestModal.classList.add('active');
    };

    window.messageUser = function() {
        // Redirect to chat with this user selected
        window.location.href = `chat.html?user=${profileUser.id}`;
    };

    // Close Modals
    document.querySelectorAll('.close-modal, .cancel-btn').forEach(btn => {
        btn.addEventListener('click', () => {
            editModal.classList.remove('active');
            if (requestModal) requestModal.classList.remove('active');
        });
    });

    // Handle Edit Profile Save
    const editForm = document.getElementById('edit-form');
    if (editForm) {
        editForm.addEventListener('submit', (e) => {
            e.preventDefault();
            
            profileUser.name = document.getElementById('edit-name').value.trim();
            profileUser.location = document.getElementById('edit-location').value.trim();
            profileUser.college = document.getElementById('edit-college').value.trim();
            profileUser.bio = document.getElementById('edit-bio').value.trim();
            profileUser.availability = document.getElementById('edit-availability').value.trim();
            
            const teachRaw = document.getElementById('edit-teach').value.trim();
            const learnRaw = document.getElementById('edit-learn').value.trim();
            
            profileUser.canTeach = teachRaw.split(',').map(s => s.trim()).filter(s => s);
            profileUser.wantsToLearn = learnRaw.split(',').map(s => s.trim()).filter(s => s);
            
            // Save to localStorage
            const userIndex = users.findIndex(u => u.id === profileUser.id);
            users[userIndex] = profileUser;
            saveUsers(users);
            setCurrentUser(profileUser);
            
            showToast('Profile updated successfully!');
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        });
    }

    // Handle Request Exchange Send
    const requestForm = document.getElementById('exchange-form');
    if (requestForm) {
        requestForm.addEventListener('submit', (e) => {
            e.preventDefault();
            const message = document.getElementById('request-message').value.trim();
            
            const requests = getRequests();
            const exists = requests.find(r => r.fromUserId === currentUser.id && r.toUserId === profileUser.id && r.status === 'pending');
            
            if (exists) {
                showToast('You already have a pending request with this user.', 'error');
                requestModal.classList.remove('active');
                return;
            }

            requests.push({
                id: Date.now(),
                fromUserId: currentUser.id,
                toUserId: profileUser.id,
                message: message,
                status: 'pending',
                date: new Date().toISOString()
            });

            saveRequests(requests);
            showToast('Request sent successfully!');
            requestModal.classList.remove('active');
        });
    }
});
