document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const users = getUsers().filter(u => u.id !== currentUser.id);

    // Mock distances and positions
    const nearbyUsers = users.slice(0, 6).map(u => {
        // Random distance between 1 and 15 km
        const distance = (Math.random() * 14 + 1).toFixed(1);
        
        // Random position on the map (10% to 90% for both top and left)
        const top = Math.floor(Math.random() * 80) + 10;
        const left = Math.floor(Math.random() * 80) + 10;
        
        return {
            ...u,
            distance: parseFloat(distance),
            top,
            left
        };
    }).sort((a, b) => a.distance - b.distance);

    const mapSimulation = document.getElementById('map-simulation');
    const nearbyGrid = document.getElementById('nearby-grid');

    function renderMap() {
        // Render current user in center
        let mapHtml = `
            <div class="map-marker me" style="top: 50%; left: 50%;">
                <div class="marker-label">You</div>
            </div>
        `;

        // Render nearby users
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
                        <p>📍 ${user.location}</p>
                        <div class="user-rating">⭐ ${user.rating.toFixed(1)}</div>
                    </div>
                </div>
                <div class="skills-section mt-1">
                    <h4>Can Teach</h4>
                    <div class="skills-list">
                        ${user.canTeach.map(s => `<span class="skill-tag">${s}</span>`).join('')}
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
});
