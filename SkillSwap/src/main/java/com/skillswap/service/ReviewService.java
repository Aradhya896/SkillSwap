package com.skillswap.service;
import com.skillswap.dto.ReviewDTO;
import com.skillswap.entity.Review;
import com.skillswap.entity.User;
import com.skillswap.exception.BadRequestException;
import com.skillswap.repository.ReviewRepository;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ReviewService {
    @Autowired ReviewRepository reviewRepository;
    @Autowired UserRepository userRepository;

    public ReviewDTO createReview(Long reviewerId, ReviewDTO dto) {
        if (reviewerId.equals(dto.getToUserId())) throw new BadRequestException("Cannot review yourself");
        
        User reviewer = userRepository.findById(reviewerId).orElseThrow();
        User reviewedUser = userRepository.findById(dto.getToUserId()).orElseThrow();

        Review review = new Review();
        review.setReviewer(reviewer);
        review.setReviewedUser(reviewedUser);
        review.setRating(dto.getRating());
        review.setComment(dto.getText());
        reviewRepository.save(review);
        
        // Update user rating
        reviewedUser.setReviewCount(reviewedUser.getReviewCount() + 1);
        double totalRating = reviewRepository.findByReviewedUserIdOrderByCreatedAtDesc(reviewedUser.getId())
                                             .stream().mapToInt(Review::getRating).sum();
        reviewedUser.setRating(totalRating / reviewedUser.getReviewCount());
        userRepository.save(reviewedUser);

        return mapToDTO(review);
    }

    public List<ReviewDTO> getUserReviews(Long userId) {
        return reviewRepository.findByReviewedUserIdOrderByCreatedAtDesc(userId)
                               .stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    private ReviewDTO mapToDTO(Review r) {
        ReviewDTO dto = new ReviewDTO();
        dto.setId(r.getId());
        dto.setFromUserId(r.getReviewer().getId());
        dto.setToUserId(r.getReviewedUser().getId());
        dto.setAuthorName(r.getReviewer().getName());
        dto.setRating(r.getRating());
        dto.setText(r.getComment());
        dto.setDate(r.getCreatedAt());
        return dto;
    }
}
