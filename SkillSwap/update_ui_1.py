import os

# PROFILE.JS
profile_js = """document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const urlParams = new URLSearchParams(window.location.search);
    const profileId = parseInt(urlParams.get('id')) || currentUser.id;
    const isOwnProfile = profileId === currentUser.id;

    let profileUser = null;

    try {
        profileUser = await fetchWithAuth(`/users/${profileId}`);
    } catch (err) {
        document.querySelector('.profile-container').innerHTML = `
            <div class="empty-state">
                <h2>User not found</h2>
                <p>The user you are looking for does not exist or server is unreachable.</p>
                <a href="browse.html" class="btn btn-primary mt-2">Back to Browse</a>
            </div>
        `;
        return;
    }

    // Render Profile Data
    document.title = `${profileUser.name} - SkillSwap`;
    document.getElementById('profile-avatar').textContent = getInitials(profileUser.name);
    document.getElementById('profile-name').textContent = profileUser.name;
    document.getElementById('profile-location').textContent = `📍 ${profileUser.location || 'Unknown'}`;
    document.getElementById('profile-college').textContent = `🎓 ${profileUser.college || 'Not specified'}`;
    document.getElementById('profile-availability').textContent = `⏰ ${profileUser.availability || 'Flexible'}`;
    document.getElementById('profile-joined').textContent = `📅 Member`;
    
    document.getElementById('stat-rating').textContent = `${profileUser.rating ? profileUser.rating.toFixed(1) : '0.0'}/5.0`;
    document.getElementById('stat-reviews').textContent = profileUser.reviewCount || 0;
    
    document.getElementById('profile-bio').textContent = profileUser.bio || '';

    // Render Skills
    const teachContainer = document.getElementById('skills-teach');
    teachContainer.innerHTML = (profileUser.skillsToTeach || []).map(s => `<span class="skill-tag">${s}</span>`).join('');

    const learnContainer = document.getElementById('skills-learn');
    learnContainer.innerHTML = (profileUser.skillsToLearn || []).map(s => `<span class="skill-tag want">${s}</span>`).join('');

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

    // Reviews
    const reviewsContainer = document.getElementById('profile-reviews');
    try {
        const allReviews = await fetchWithAuth(`/users/${profileId}/reviews`);
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
    } catch (e) {
        reviewsContainer.innerHTML = `<p class="text-muted">Could not load reviews.</p>`;
    }

    // Modals
    const editModal = document.getElementById('edit-modal');
    const requestModal = document.getElementById('request-modal');
    
    window.openEditModal = function() {
        document.getElementById('edit-name').value = profileUser.name || '';
        document.getElementById('edit-location').value = profileUser.location || '';
        document.getElementById('edit-college').value = profileUser.college || '';
        document.getElementById('edit-bio').value = profileUser.bio || '';
        document.getElementById('edit-teach').value = (profileUser.skillsToTeach || []).join(', ');
        document.getElementById('edit-learn').value = (profileUser.skillsToLearn || []).join(', ');
        document.getElementById('edit-availability').value = profileUser.availability || '';
        editModal.classList.add('active');
    };

    window.openRequestModal = function() {
        document.getElementById('modal-user-name').textContent = profileUser.name;
        document.getElementById('modal-teach-skills').textContent = (profileUser.skillsToTeach || []).join(', ');
        document.getElementById('modal-learn-skills').textContent = (profileUser.skillsToLearn || []).join(', ');
        document.getElementById('request-message').value = '';
        requestModal.classList.add('active');
    };

    window.messageUser = function() {
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
        editForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            
            const updatedProfile = {
                name: document.getElementById('edit-name').value.trim(),
                location: document.getElementById('edit-location').value.trim(),
                college: document.getElementById('edit-college').value.trim(),
                bio: document.getElementById('edit-bio').value.trim(),
                availability: document.getElementById('edit-availability').value.trim(),
                skillsToTeach: document.getElementById('edit-teach').value.trim().split(',').map(s => s.trim()).filter(s => s),
                skillsToLearn: document.getElementById('edit-learn').value.trim().split(',').map(s => s.trim()).filter(s => s)
            };
            
            try {
                const res = await fetchWithAuth(`/users/${currentUser.id}`, {
                    method: 'PUT',
                    body: updatedProfile
                });
                
                showToast('Profile updated successfully!');
                
                // Update local storage user info if changed
                const userSession = getCurrentUser();
                userSession.name = updatedProfile.name;
                setCurrentUser(userSession);
                
                setTimeout(() => {
                    window.location.reload();
                }, 1000);
            } catch (err) {
                showToast('Unable to update profile.', 'error');
            }
        });
    }

    // Handle Request Exchange Send
    const requestForm = document.getElementById('exchange-form');
    if (requestForm) {
        requestForm.addEventListener('submit', async (e) => {
            e.preventDefault();
            const message = document.getElementById('request-message').value.trim();
            
            try {
                await fetchWithAuth('/requests', {
                    method: 'POST',
                    body: { toUserId: profileUser.id, message }
                });
                showToast('Request sent successfully!');
                requestModal.classList.remove('active');
            } catch (err) {
                showToast(err.message || 'Unable to send request.', 'error');
                requestModal.classList.remove('active');
            }
        });
    }
});
"""

with open("js/profile.js", "w", encoding="utf-8") as f:
    f.write(profile_js)


# REQUESTS.JS
requests_js = """document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();
    
    const incomingTabBtn = document.getElementById('tab-incoming');
    const sentTabBtn = document.getElementById('tab-sent');
    const incomingContent = document.getElementById('content-incoming');
    const sentContent = document.getElementById('content-sent');

    // Tab switching
    incomingTabBtn.addEventListener('click', () => {
        incomingTabBtn.classList.add('active');
        sentTabBtn.classList.remove('active');
        incomingContent.classList.add('active');
        sentContent.classList.remove('active');
    });

    sentTabBtn.addEventListener('click', () => {
        sentTabBtn.classList.add('active');
        incomingTabBtn.classList.remove('active');
        sentContent.classList.add('active');
        incomingContent.classList.remove('active');
    });

    async function loadRequests() {
        try {
            const incomingReqs = await fetchWithAuth('/requests/incoming');
            const sentReqs = await fetchWithAuth('/requests/sent');
            renderRequestList(incomingReqs, incomingContent, true);
            renderRequestList(sentReqs, sentContent, false);
        } catch (err) {
            console.error(err);
            incomingContent.innerHTML = `<div class="empty-state">Unable to connect to server.</div>`;
        }
    }

    function renderRequestList(requests, container, isIncoming) {
        if (requests.length === 0) {
            container.innerHTML = `
                <div class="empty-state">
                    <h3>No requests found</h3>
                    <p>You don't have any ${isIncoming ? 'incoming' : 'sent'} requests yet.</p>
                </div>
            `;
            return;
        }

        container.innerHTML = requests.map(req => {
            const otherUserId = isIncoming ? req.fromUserId : req.toUserId;
            const otherUserName = isIncoming ? req.fromUserName : req.toUserName;
            
            const dateStr = new Date(req.date).toLocaleDateString();
            let actionsHtml = '';
            
            if (isIncoming) {
                if (req.status === 'pending') {
                    actionsHtml = `
                        <div class="req-actions">
                            <button class="btn btn-success" onclick="updateRequestStatus(${req.id}, 'accept')">Accept</button>
                            <button class="btn btn-danger" onclick="updateRequestStatus(${req.id}, 'reject')">Reject</button>
                            <a href="profile.html?id=${otherUserId}" class="btn btn-secondary">View Profile</a>
                        </div>
                    `;
                } else {
                    actionsHtml = `
                        <div class="req-actions">
                            <span class="status-badge status-${req.status}">${req.status.charAt(0).toUpperCase() + req.status.slice(1)}</span>
                            ${req.status === 'accepted' ? `<a href="chat.html?user=${otherUserId}" class="btn btn-primary btn-sm">Chat Now</a>` : ''}
                        </div>
                    `;
                }
            } else {
                actionsHtml = `
                    <div class="req-actions">
                        <span class="status-badge status-${req.status}">${req.status.charAt(0).toUpperCase() + req.status.slice(1)}</span>
                        ${req.status === 'accepted' ? `<a href="chat.html?user=${otherUserId}" class="btn btn-primary btn-sm">Chat Now</a>` : ''}
                        <a href="profile.html?id=${otherUserId}" class="btn btn-secondary btn-sm">View Profile</a>
                    </div>
                `;
            }

            return `
                <div class="request-card">
                    <div class="req-avatar">${getInitials(otherUserName)}</div>
                    <div class="req-content">
                        <div class="req-header">
                            <div>
                                <h3>${isIncoming ? 'From' : 'To'}: ${otherUserName}</h3>
                            </div>
                            <div class="req-date">${dateStr}</div>
                        </div>
                        <div class="req-message">"${req.message}"</div>
                        ${actionsHtml}
                    </div>
                </div>
            `;
        }).join('');
    }

    window.updateRequestStatus = async function(reqId, action) {
        try {
            await fetchWithAuth(`/requests/${reqId}/${action}`, { method: 'PUT' });
            showToast(`Request ${action}ed successfully!`);
            loadRequests();
        } catch (err) {
            showToast(err.message || 'Unable to update request.', 'error');
        }
    };

    // Initial render
    loadRequests();
});
"""

with open("js/requests.js", "w", encoding="utf-8") as f:
    f.write(requests_js)
