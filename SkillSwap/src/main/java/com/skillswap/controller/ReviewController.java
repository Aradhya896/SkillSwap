package com.skillswap.controller;
import com.skillswap.dto.ApiResponse;
import com.skillswap.dto.ReviewDTO;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.ReviewService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api")
public class ReviewController {
    @Autowired ReviewService reviewService;

    @PostMapping("/reviews")
    public ResponseEntity<?> createReview(@Valid @RequestBody ReviewDTO reviewDTO, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Review submitted", reviewService.createReview(userDetails.getId(), reviewDTO)));
    }

    @GetMapping("/users/{id}/reviews")
    public ResponseEntity<?> getUserReviews(@PathVariable Long id) {
        return ResponseEntity.ok(reviewService.getUserReviews(id));
    }
}
