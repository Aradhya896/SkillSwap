document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const users = getUsers();
    
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

    function renderRequests() {
        const requests = getRequests();
        
        const incomingReqs = requests.filter(r => r.toUserId === currentUser.id);
        const sentReqs = requests.filter(r => r.fromUserId === currentUser.id);

        renderRequestList(incomingReqs, incomingContent, true);
        renderRequestList(sentReqs, sentContent, false);
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

        // Sort by date descending
        requests.sort((a, b) => new Date(b.date) - new Date(a.date));

        container.innerHTML = requests.map(req => {
            const otherUserId = isIncoming ? req.fromUserId : req.toUserId;
            const otherUser = users.find(u => u.id === otherUserId);
            
            if (!otherUser) return ''; // User might have been deleted

            const dateStr = new Date(req.date).toLocaleDateString();
            
            let actionsHtml = '';
            
            if (isIncoming) {
                if (req.status === 'pending') {
                    actionsHtml = `
                        <div class="req-actions">
                            <button class="btn btn-success" onclick="updateRequestStatus(${req.id}, 'accepted')">Accept</button>
                            <button class="btn btn-danger" onclick="updateRequestStatus(${req.id}, 'rejected')">Reject</button>
                            <a href="profile.html?id=${otherUser.id}" class="btn btn-secondary">View Profile</a>
                        </div>
                    `;
                } else {
                    actionsHtml = `
                        <div class="req-actions">
                            <span class="status-badge status-${req.status}">${req.status.charAt(0).toUpperCase() + req.status.slice(1)}</span>
                            ${req.status === 'accepted' ? `<a href="chat.html?user=${otherUser.id}" class="btn btn-primary btn-sm">Chat Now</a>` : ''}
                        </div>
                    `;
                }
            } else {
                actionsHtml = `
                    <div class="req-actions">
                        <span class="status-badge status-${req.status}">${req.status.charAt(0).toUpperCase() + req.status.slice(1)}</span>
                        ${req.status === 'accepted' ? `<a href="chat.html?user=${otherUser.id}" class="btn btn-primary btn-sm">Chat Now</a>` : ''}
                        <a href="profile.html?id=${otherUser.id}" class="btn btn-secondary btn-sm">View Profile</a>
                    </div>
                `;
            }

            return `
                <div class="request-card">
                    <div class="req-avatar">${getInitials(otherUser.name)}</div>
                    <div class="req-content">
                        <div class="req-header">
                            <div>
                                <h3>${isIncoming ? 'From' : 'To'}: ${otherUser.name}</h3>
                                <div class="req-skills">
                                    <strong>They teach:</strong> ${otherUser.canTeach.join(', ')} <br>
                                    <strong>They want:</strong> ${otherUser.wantsToLearn.join(', ')}
                                </div>
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

    window.updateRequestStatus = function(reqId, newStatus) {
        const requests = getRequests();
        const reqIndex = requests.findIndex(r => r.id === reqId);
        
        if (reqIndex !== -1) {
            requests[reqIndex].status = newStatus;
            saveRequests(requests);
            
            showToast(`Request ${newStatus}!`);
            renderRequests();
        }
    };

    // Initial render
    renderRequests();
});
