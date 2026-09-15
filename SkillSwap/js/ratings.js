document.addEventListener('DOMContentLoaded', () => {
    requireAuth();

    const currentUser = getCurrentUser();
    const urlParams = new URLSearchParams(window.location.search);
    const targetUserId = parseInt(urlParams.get('id'));
    
    if (!targetUserId || targetUserId === currentUser.id) {
        window.location.href = 'browse.html';
        return;
    }

    const users = getUsers();
    const targetUser = users.find(u => u.id === targetUserId);
    
    if (!targetUser) {
        window.location.href = 'browse.html';
        return;
    }

    document.getElementById('target-avatar').textContent = getInitials(targetUser.name);
    document.getElementById('target-name').textContent = targetUser.name;

    const ratingForm = document.getElementById('rating-form');
    
    ratingForm.addEventListener('submit', (e) => {
        e.preventDefault();
        
        // Find selected star
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

        const reviews = getReviews();
        
        const newReview = {
            id: Date.now(),
            fromUserId: currentUser.id,
            toUserId: targetUser.id,
            authorName: currentUser.name,
            rating: ratingValue,
            text: reviewText,
            date: new Date().toISOString()
        };
        
        reviews.push(newReview);
        saveReviews(reviews);
        
        // Update user's average rating in users array
        const userReviews = reviews.filter(r => r.toUserId === targetUser.id);
        const avgRating = userReviews.reduce((sum, r) => sum + r.rating, 0) / userReviews.length;
        
        const targetUserIndex = users.findIndex(u => u.id === targetUser.id);
        users[targetUserIndex].rating = avgRating;
        if (!users[targetUserIndex].reviews) users[targetUserIndex].reviews = [];
        users[targetUserIndex].reviews.push(newReview.id);
        
        saveUsers(users);
        
        showToast('Review submitted successfully!');
        setTimeout(() => {
            window.location.href = `profile.html?id=${targetUser.id}`;
        }, 1500);
    });
});
