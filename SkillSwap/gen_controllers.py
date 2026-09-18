import os

files = {
    # CONTROLLERS
    "src/main/java/com/skillswap/controller/AuthController.java": """package com.skillswap.controller;
import com.skillswap.dto.ApiResponse;
import com.skillswap.dto.LoginRequest;
import com.skillswap.dto.RegisterRequest;
import com.skillswap.service.AuthService;
import jakarta.validation.Valid;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {
    @Autowired AuthService authService;

    @PostMapping("/login")
    public ResponseEntity<?> authenticateUser(@Valid @RequestBody LoginRequest loginRequest) {
        return ResponseEntity.ok(authService.authenticateUser(loginRequest));
    }

    @PostMapping("/register")
    public ResponseEntity<?> registerUser(@Valid @RequestBody RegisterRequest signUpRequest) {
        return ResponseEntity.ok(new ApiResponse(true, "User registered successfully", authService.registerUser(signUpRequest)));
    }
}
""",
    "src/main/java/com/skillswap/controller/UserController.java": """package com.skillswap.controller;
import com.skillswap.dto.ApiResponse;
import com.skillswap.dto.UserResponse;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired UserService userService;

    @GetMapping
    public ResponseEntity<?> searchUsers(
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) Double minRating) {
        if (search == null && location == null && minRating == null) {
            return ResponseEntity.ok(userService.getAllUsers());
        }
        return ResponseEntity.ok(userService.searchUsers(search, location, minRating));
    }

    @GetMapping("/nearby")
    public ResponseEntity<?> getNearbyUsers(@RequestParam String location) {
        return ResponseEntity.ok(userService.searchUsers(null, location, null));
    }

    @GetMapping("/me")
    public ResponseEntity<?> getCurrentUser(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(userService.getUserById(userDetails.getId()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUserById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateUser(@PathVariable Long id, @RequestBody UserResponse userDto, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        if (!id.equals(userDetails.getId())) return ResponseEntity.status(403).body(new ApiResponse(false, "Unauthorized"));
        return ResponseEntity.ok(new ApiResponse(true, "Profile updated", userService.updateUser(id, userDto)));
    }
}
""",
    "src/main/java/com/skillswap/controller/ExchangeRequestController.java": """package com.skillswap.controller;
import com.skillswap.dto.ApiResponse;
import com.skillswap.dto.ExchangeRequestDTO;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.ExchangeRequestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/requests")
public class ExchangeRequestController {
    @Autowired ExchangeRequestService requestService;

    @PostMapping
    public ResponseEntity<?> sendRequest(@RequestBody ExchangeRequestDTO requestDTO, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Request sent", requestService.createRequest(userDetails.getId(), requestDTO)));
    }

    @GetMapping("/incoming")
    public ResponseEntity<?> getIncomingRequests(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(requestService.getIncomingRequests(userDetails.getId()));
    }

    @GetMapping("/sent")
    public ResponseEntity<?> getSentRequests(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(requestService.getSentRequests(userDetails.getId()));
    }

    @PutMapping("/{id}/accept")
    public ResponseEntity<?> acceptRequest(@PathVariable Long id, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Request accepted", requestService.updateRequestStatus(id, userDetails.getId(), "accepted")));
    }

    @PutMapping("/{id}/reject")
    public ResponseEntity<?> rejectRequest(@PathVariable Long id, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Request rejected", requestService.updateRequestStatus(id, userDetails.getId(), "rejected")));
    }
}
""",
    "src/main/java/com/skillswap/controller/ChatController.java": """package com.skillswap.controller;
import com.skillswap.dto.MessageDTO;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/conversations")
public class ChatController {
    @Autowired ChatService chatService;

    @GetMapping
    public ResponseEntity<?> getUserConversations(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(chatService.getUserConversations(userDetails.getId()));
    }

    @GetMapping("/{id}/messages")
    public ResponseEntity<?> getMessages(@PathVariable Long id) {
        return ResponseEntity.ok(chatService.getMessages(id));
    }

    @PostMapping("/{id}/messages")
    public ResponseEntity<?> sendMessage(@PathVariable Long id, @RequestBody MessageDTO messageDTO, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        // Here ID is conversation ID, but the service creates or finds conversation based on toUserId 
        // to simplify the flow as per the frontend implementation.
        return ResponseEntity.ok(chatService.sendMessage(userDetails.getId(), messageDTO));
    }
}
""",
    "src/main/java/com/skillswap/controller/ReviewController.java": """package com.skillswap.controller;
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
""",
    "src/main/java/com/skillswap/config/DataInitializer.java": """package com.skillswap.config;
import com.skillswap.entity.User;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import java.util.Set;

@Component
public class DataInitializer implements CommandLineRunner {
    @Autowired UserRepository userRepository;
    @Autowired PasswordEncoder passwordEncoder;

    @Override
    public void run(String... args) throws Exception {
        if (userRepository.count() == 0) {
            String encodedPassword = passwordEncoder.encode("123456");

            User demo = new User();
            demo.setName("Demo User");
            demo.setEmail("demo@skillswap.com");
            demo.setPassword(encodedPassword);
            demo.setCollege("Pune University");
            demo.setLocation("Pune");
            demo.setBio("I am a demo user exploring the SkillSwap platform.");
            demo.setAvailability("Flexible");
            demo.setSkillsToTeach(Set.of("Photography", "Excel"));
            demo.setSkillsToLearn(Set.of("Java", "Public Speaking"));
            demo.setRating(5.0);
            demo.setReviewCount(1);
            userRepository.save(demo);

            User user1 = new User();
            user1.setName("Aarav Sharma");
            user1.setEmail("aarav@example.com");
            user1.setPassword(encodedPassword);
            user1.setCollege("Galgotias University");
            user1.setLocation("Greater Noida");
            user1.setBio("Computer science student interested in web development.");
            user1.setAvailability("Weekends");
            user1.setSkillsToTeach(Set.of("Java", "HTML", "CSS"));
            user1.setSkillsToLearn(Set.of("Python", "Machine Learning"));
            user1.setRating(4.7);
            user1.setReviewCount(5);
            userRepository.save(user1);

            User user2 = new User();
            user2.setName("Priya Patel");
            user2.setEmail("priya@example.com");
            user2.setPassword(encodedPassword);
            user2.setCollege("IIT Bombay");
            user2.setLocation("Mumbai");
            user2.setBio("UI/UX Designer who loves creating beautiful interfaces.");
            user2.setAvailability("Evenings");
            user2.setSkillsToTeach(Set.of("UI/UX", "Figma", "Design"));
            user2.setSkillsToLearn(Set.of("JavaScript", "React"));
            user2.setRating(4.9);
            user2.setReviewCount(10);
            userRepository.save(user2);
            
            System.out.println("Sample data initialized!");
        }
    }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
