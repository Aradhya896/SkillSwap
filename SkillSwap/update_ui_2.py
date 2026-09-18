import os

# CHAT.JS
chat_js = """document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const contactsList = document.getElementById('contacts-list');
    const chatArea = document.getElementById('chat-area');
    
    let activeChatUserId = null;
    let activeConversationId = null;
    let activeContactName = '';
    let contacts = [];
    
    const urlParams = new URLSearchParams(window.location.search);
    const targetUserIdParam = urlParams.get('user');
    
    if (targetUserIdParam) {
        activeChatUserId = parseInt(targetUserIdParam);
    }

    async function loadContacts() {
        try {
            const conversations = await fetchWithAuth('/conversations');
            contacts = conversations.map(c => ({
                id: c.otherUser.id,
                name: c.otherUser.name,
                conversationId: c.id
            }));
            
            // Ensure URL param user is in contacts list (might be first time chatting)
            if (activeChatUserId && !contacts.find(c => c.id === activeChatUserId)) {
                try {
                    const u = await fetchWithAuth(`/users/${activeChatUserId}`);
                    contacts.push({ id: u.id, name: u.name, conversationId: null });
                } catch(e) {}
            }
            
            renderContacts();
            
            if (activeChatUserId) {
                const contact = contacts.find(c => c.id === activeChatUserId);
                if (contact) {
                    activeConversationId = contact.conversationId;
                    activeContactName = contact.name;
                    renderChatArea();
                }
            }
        } catch (err) {
            console.error(err);
        }
    }

    function renderContacts() {
        if (contacts.length === 0) {
            contactsList.innerHTML = `<div class="empty-state" style="padding: 20px;">No connections yet. Send a message to someone to start chatting!</div>`;
            return;
        }
        
        contactsList.innerHTML = contacts.map(contact => {
            return `
                <div class="contact-item ${activeChatUserId === contact.id ? 'active' : ''}" onclick="openChat(${contact.id}, ${contact.conversationId}, '${contact.name.replace(/'/g, "\\'")}')">
                    <div class="contact-avatar">${getInitials(contact.name)}</div>
                    <div class="contact-info">
                        <div class="contact-name">${contact.name}</div>
                        <div class="contact-last-msg">Click to view messages</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    window.openChat = function(userId, conversationId, userName) {
        activeChatUserId = userId;
        activeConversationId = conversationId;
        activeContactName = userName;
        renderContacts();
        renderChatArea();
    };

    async function renderChatArea() {
        if (!activeChatUserId) {
            chatArea.innerHTML = `
                <div class="no-chat-selected">
                    <div class="no-chat-icon">💬</div>
                    <h3>Select a conversation</h3>
                    <p>Choose a contact from the sidebar to start chatting</p>
                </div>
            `;
            return;
        }

        chatArea.innerHTML = `
            <div class="chat-header">
                <div class="contact-avatar">${getInitials(activeContactName)}</div>
                <div class="chat-header-info">
                    <h3>${activeContactName}</h3>
                    <div class="status-online">● Online</div>
                </div>
                <div style="margin-left: auto;">
                    <a href="profile.html?id=${activeChatUserId}" class="btn btn-secondary btn-sm">Profile</a>
                    <a href="ratings.html?id=${activeChatUserId}" class="btn btn-primary btn-sm">Leave Review</a>
                </div>
            </div>
            <div class="messages-area" id="messages-area">
                <div style="text-align:center; margin-top:20px; color:gray;">Loading messages...</div>
            </div>
            <form class="chat-input-area" id="chat-form">
                <input type="text" class="chat-input" id="message-input" placeholder="Type a message..." required autocomplete="off">
                <button type="submit" class="send-btn">➤</button>
            </form>
        `;

        document.getElementById('chat-form').addEventListener('submit', (e) => {
            e.preventDefault();
            sendMessage();
        });

        loadMessages();
    }

    async function loadMessages() {
        const messagesArea = document.getElementById('messages-area');
        if (!activeConversationId) {
            messagesArea.innerHTML = `
                <div style="text-align:center; color: var(--text-muted); margin-top: 20px;">
                    Send a message to start the conversation with ${activeContactName}.
                </div>
            `;
            return;
        }

        try {
            const msgs = await fetchWithAuth(`/conversations/${activeConversationId}/messages`);
            
            if (msgs.length === 0) {
                messagesArea.innerHTML = `<div style="text-align:center; color: var(--text-muted); margin-top: 20px;">Send a message to start the conversation.</div>`;
                return;
            }

            messagesArea.innerHTML = msgs.map(m => {
                const isSent = m.fromUserId === currentUser.id;
                const timeStr = new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
                return `
                    <div class="message-bubble ${isSent ? 'msg-sent' : 'msg-received'}">
                        ${m.text}
                        <span class="msg-time">${timeStr}</span>
                    </div>
                `;
            }).join('');
            messagesArea.scrollTop = messagesArea.scrollHeight;
        } catch (err) {
            messagesArea.innerHTML = `<div style="text-align:center; color: red;">Failed to load messages.</div>`;
        }
    }

    async function sendMessage() {
        const input = document.getElementById('message-input');
        const text = input.value.trim();
        if (!text) return;

        try {
            await fetchWithAuth(`/conversations/0/messages`, {
                method: 'POST',
                body: { toUserId: activeChatUserId, text }
            });
            input.value = '';
            
            // If it was a new conversation, we need to reload contacts to get conversationId
            if (!activeConversationId) {
                await loadContacts(); // This will auto-load messages too via openChat
            } else {
                await loadMessages();
            }
        } catch (err) {
            showToast('Unable to send message.', 'error');
        }
    }

    // Initial render
    loadContacts();
});
"""

with open("js/chat.js", "w", encoding="utf-8") as f:
    f.write(chat_js)


# RATINGS.JS
ratings_js = """document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const urlParams = new URLSearchParams(window.location.search);
    const targetUserId = parseInt(urlParams.get('id'));
    
    if (!targetUserId || targetUserId === currentUser.id) {
        window.location.href = 'browse.html';
        return;
    }

    let targetUser = null;
    try {
        targetUser = await fetchWithAuth(`/users/${targetUserId}`);
        document.getElementById('target-avatar').textContent = getInitials(targetUser.name);
        document.getElementById('target-name').textContent = targetUser.name;
    } catch (err) {
        window.location.href = 'browse.html';
        return;
    }

    const ratingForm = document.getElementById('rating-form');
    
    ratingForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const selectedStar = document.querySelector('.star-input:checked');
        if (!selectedStar) {
            showToast('Please select a star rating', 'error');
            return;
        }
        
        const ratingValue = parseInt(selectedStar.value);
        const reviewText = document.getElementById('review-text').value.trim();
        
        if (!reviewText) {
            showToast('Please write a review', 'error');
            return;
        }

        try {
            await fetchWithAuth('/reviews', {
                method: 'POST',
                body: { toUserId: targetUserId, rating: ratingValue, text: reviewText }
            });
            showToast('Review submitted successfully!');
            setTimeout(() => {
                window.location.href = `profile.html?id=${targetUserId}`;
            }, 1500);
        } catch (err) {
            showToast(err.message || 'Unable to submit review.', 'error');
        }
    });
});
"""

with open("js/ratings.js", "w", encoding="utf-8") as f:
    f.write(ratings_js)


# NEARBY.JS
nearby_js = """document.addEventListener('DOMContentLoaded', async () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const mapSimulation = document.getElementById('map-simulation');
    const nearbyGrid = document.getElementById('nearby-grid');

    try {
        // We will just fetch all users and mock distance for UI demo since no real geo-coords exist.
        // OR we could call the endpoint with location search. Let's just use /users
        const allUsers = await fetchWithAuth('/users');
        const users = allUsers.filter(u => u.id !== currentUser.id);

        const nearbyUsers = users.slice(0, 6).map(u => {
            const distance = (Math.random() * 14 + 1).toFixed(1);
            const top = Math.floor(Math.random() * 80) + 10;
            const left = Math.floor(Math.random() * 80) + 10;
            return { ...u, distance: parseFloat(distance), top, left };
        }).sort((a, b) => a.distance - b.distance);

        function renderMap() {
            let mapHtml = `<div class="map-marker me" style="top: 50%; left: 50%;"><div class="marker-label">You</div></div>`;
            nearbyUsers.forEach(user => {
                mapHtml += `
                    <div class="map-marker" style="top: ${user.top}%; left: ${user.left}%;" title="${user.name} - ${user.distance}km">
                        <div class="marker-label">${user.name.split(' ')[0]}</div>
                    </div>
                `;
            });
            mapSimulation.innerHTML = mapHtml;
        }

        function renderList() {
            if (nearbyUsers.length === 0) {
                nearbyGrid.innerHTML = `
                    <div class="empty-state" style="grid-column: 1 / -1;">
                        <h2>No nearby skill partners found</h2>
                        <p>Try again later or update your location.</p>
                    </div>
                `;
                return;
            }

            nearbyGrid.innerHTML = nearbyUsers.map(user => `
                <div class="card user-card">
                    <div class="distance-badge">🚗 ${user.distance} km away</div>
                    <div class="user-card-header" style="margin-bottom: 10px;">
                        <div class="avatar">${getInitials(user.name)}</div>
                        <div class="user-info">
                            <h3>${user.name}</h3>
                            <p>📍 ${user.location || 'Unknown'}</p>
                            <div class="user-rating">⭐ ${user.rating ? user.rating.toFixed(1) : '0.0'}</div>
                        </div>
                    </div>
                    <div class="skills-section mt-1">
                        <h4>Can Teach</h4>
                        <div class="skills-list">
                            ${(user.skillsToTeach || []).map(s => `<span class="skill-tag">${s}</span>`).join('')}
                        </div>
                    </div>
                    <div class="card-actions mt-2">
                        <a href="profile.html?id=${user.id}" class="btn btn-secondary btn-sm">View Profile</a>
                    </div>
                </div>
            `).join('');
        }

        renderMap();
        renderList();

    } catch (err) {
        console.error(err);
        nearbyGrid.innerHTML = `<div class="empty-state" style="grid-column: 1 / -1;">Unable to connect to server.</div>`;
    }
});
"""

with open("js/nearby.js", "w", encoding="utf-8") as f:
    f.write(nearby_js)


# SETTINGS.JS
settings_js = """document.addEventListener('DOMContentLoaded', () => {
    requireAuth();
    
    document.getElementById('password-form').addEventListener('submit', (e) => {
        e.preventDefault();
        showToast('Password reset endpoint not fully implemented in demo, but you would normally call /auth/reset here', 'success');
        e.target.reset();
    });

    window.deleteAccount = function() {
        if (confirm('Are you sure you want to delete your account? This action cannot be undone.')) {
            // Ideally call DELETE /api/users/me
            showToast('Account deletion simulated.');
            logout();
        }
    };
});
"""

with open("js/settings.js", "w", encoding="utf-8") as f:
    f.write(settings_js)
