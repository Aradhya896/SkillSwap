document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const users = getUsers();
    const requests = getRequests();
    
    // Get users we have accepted requests with
    const connectedUserIds = new Set();
    requests.forEach(r => {
        if (r.status === 'accepted') {
            if (r.fromUserId === currentUser.id) connectedUserIds.add(r.toUserId);
            if (r.toUserId === currentUser.id) connectedUserIds.add(r.fromUserId);
        }
    });

    const contacts = users.filter(u => connectedUserIds.has(u.id));
    
    const contactsList = document.getElementById('contacts-list');
    const chatArea = document.getElementById('chat-area');
    
    let activeChatUserId = null;
    
    // Check if URL has a specific user to chat with
    const urlParams = new URLSearchParams(window.location.search);
    const targetUserIdParam = urlParams.get('user');
    
    if (targetUserIdParam) {
        activeChatUserId = parseInt(targetUserIdParam);
        // Ensure this user is in our contacts (or just allow it for demo purposes)
        if (!contacts.find(c => c.id === activeChatUserId)) {
            const userToAdd = users.find(u => u.id === activeChatUserId);
            if (userToAdd) contacts.push(userToAdd);
        }
    }

    function renderContacts() {
        if (contacts.length === 0) {
            contactsList.innerHTML = `<div class="empty-state" style="padding: 20px;">No connections yet. Accept a request to start chatting!</div>`;
            return;
        }

        const messages = getMessages();
        
        contactsList.innerHTML = contacts.map(contact => {
            // Find last message
            const chatMsgs = messages.filter(m => 
                (m.fromUserId === currentUser.id && m.toUserId === contact.id) ||
                (m.fromUserId === contact.id && m.toUserId === currentUser.id)
            ).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));
            
            const lastMsg = chatMsgs.length > 0 ? chatMsgs[chatMsgs.length - 1].text : 'No messages yet';

            return `
                <div class="contact-item ${activeChatUserId === contact.id ? 'active' : ''}" onclick="openChat(${contact.id})">
                    <div class="contact-avatar">${getInitials(contact.name)}</div>
                    <div class="contact-info">
                        <div class="contact-name">${contact.name}</div>
                        <div class="contact-last-msg">${lastMsg}</div>
                    </div>
                </div>
            `;
        }).join('');
    }

    window.openChat = function(userId) {
        activeChatUserId = userId;
        renderContacts();
        renderChatArea();
    };

    function renderChatArea() {
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

        const contact = users.find(u => u.id === activeChatUserId);
        
        chatArea.innerHTML = `
            <div class="chat-header">
                <div class="contact-avatar">${getInitials(contact.name)}</div>
                <div class="chat-header-info">
                    <h3>${contact.name}</h3>
                    <div class="status-online">● Online</div>
                </div>
                <div style="margin-left: auto;">
                    <a href="profile.html?id=${contact.id}" class="btn btn-secondary btn-sm">Profile</a>
                    <a href="ratings.html?id=${contact.id}" class="btn btn-primary btn-sm">Leave Review</a>
                </div>
            </div>
            <div class="messages-area" id="messages-area">
                <!-- Messages go here -->
            </div>
            <form class="chat-input-area" id="chat-form">
                <input type="text" class="chat-input" id="message-input" placeholder="Type a message..." required autocomplete="off">
                <button type="submit" class="send-btn">➤</button>
            </form>
        `;

        renderMessages();

        document.getElementById('chat-form').addEventListener('submit', (e) => {
            e.preventDefault();
            sendMessage();
        });
    }

    function renderMessages() {
        const messagesArea = document.getElementById('messages-area');
        if (!messagesArea) return;

        const allMessages = getMessages();
        const chatMsgs = allMessages.filter(m => 
            (m.fromUserId === currentUser.id && m.toUserId === activeChatUserId) ||
            (m.fromUserId === activeChatUserId && m.toUserId === currentUser.id)
        ).sort((a, b) => new Date(a.timestamp) - new Date(b.timestamp));

        if (chatMsgs.length === 0) {
            messagesArea.innerHTML = `
                <div style="text-align:center; color: var(--text-muted); margin-top: 20px;">
                    Send a message to start the conversation with ${users.find(u=>u.id===activeChatUserId).name}.
                </div>
            `;
            return;
        }

        messagesArea.innerHTML = chatMsgs.map(m => {
            const isSent = m.fromUserId === currentUser.id;
            const timeStr = new Date(m.timestamp).toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
            return `
                <div class="message-bubble ${isSent ? 'msg-sent' : 'msg-received'}">
                    ${m.text}
                    <span class="msg-time">${timeStr}</span>
                </div>
            `;
        }).join('');

        // Scroll to bottom
        messagesArea.scrollTop = messagesArea.scrollHeight;
    }

    function sendMessage() {
        const input = document.getElementById('message-input');
        const text = input.value.trim();
        if (!text) return;

        const messages = getMessages();
        messages.push({
            id: Date.now(),
            fromUserId: currentUser.id,
            toUserId: activeChatUserId,
            text: text,
            timestamp: new Date().toISOString()
        });

        saveMessages(messages);
        input.value = '';
        renderMessages();
        renderContacts(); // update last message in sidebar
    }

    // Initial render
    renderContacts();
    if (activeChatUserId) {
        renderChatArea();
    } else {
        chatArea.innerHTML = `
            <div class="no-chat-selected">
                <div class="no-chat-icon">💬</div>
                <h3>Select a conversation</h3>
                <p>Choose a contact from the sidebar to start chatting</p>
            </div>
        `;
    }
});
