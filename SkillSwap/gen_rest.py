import os

files = {
    # REPOSITORIES
    "src/main/java/com/skillswap/repository/UserRepository.java": """package com.skillswap.repository;
import com.skillswap.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    Boolean existsByEmail(String email);
    
    @Query("SELECT DISTINCT u FROM User u LEFT JOIN u.skillsToTeach t LEFT JOIN u.skillsToLearn l WHERE " +
           "(:search IS NULL OR LOWER(u.name) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(u.location) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(t) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(l) LIKE LOWER(CONCAT('%', :search, '%'))) AND " +
           "(:location IS NULL OR LOWER(u.location) LIKE LOWER(CONCAT('%', :location, '%'))) AND " +
           "(:minRating IS NULL OR u.rating >= :minRating)")
    List<User> searchUsers(@Param("search") String search, @Param("location") String location, @Param("minRating") Double minRating);
}
""",
    "src/main/java/com/skillswap/repository/ExchangeRequestRepository.java": """package com.skillswap.repository;
import com.skillswap.entity.ExchangeRequest;
import com.skillswap.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface ExchangeRequestRepository extends JpaRepository<ExchangeRequest, Long> {
    List<ExchangeRequest> findBySenderId(Long senderId);
    List<ExchangeRequest> findByReceiverId(Long receiverId);
    Optional<ExchangeRequest> findBySenderAndReceiverAndStatus(User sender, User receiver, ExchangeRequest.RequestStatus status);
}
""",
    "src/main/java/com/skillswap/repository/ConversationRepository.java": """package com.skillswap.repository;
import com.skillswap.entity.Conversation;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface ConversationRepository extends JpaRepository<Conversation, Long> {
    @Query("SELECT c FROM Conversation c WHERE c.userOne.id = :userId OR c.userTwo.id = :userId")
    List<Conversation> findByUserId(@Param("userId") Long userId);
    
    @Query("SELECT c FROM Conversation c WHERE (c.userOne.id = :userId1 AND c.userTwo.id = :userId2) OR (c.userOne.id = :userId2 AND c.userTwo.id = :userId1)")
    Optional<Conversation> findByUsers(@Param("userId1") Long userId1, @Param("userId2") Long userId2);
}
""",
    "src/main/java/com/skillswap/repository/MessageRepository.java": """package com.skillswap.repository;
import com.skillswap.entity.Message;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface MessageRepository extends JpaRepository<Message, Long> {
    List<Message> findByConversationIdOrderByTimestampAsc(Long conversationId);
}
""",
    "src/main/java/com/skillswap/repository/ReviewRepository.java": """package com.skillswap.repository;
import com.skillswap.entity.Review;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;

@Repository
public interface ReviewRepository extends JpaRepository<Review, Long> {
    List<Review> findByReviewedUserIdOrderByCreatedAtDesc(Long reviewedUserId);
}
""",

    # EXCEPTIONS
    "src/main/java/com/skillswap/exception/GlobalExceptionHandler.java": """package com.skillswap.exception;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.MethodArgumentNotValidException;
import org.springframework.web.bind.annotation.ControllerAdvice;
import org.springframework.web.bind.annotation.ExceptionHandler;
import java.util.HashMap;
import java.util.Map;

@ControllerAdvice
public class GlobalExceptionHandler {

    @ExceptionHandler(ResourceNotFoundException.class)
    public ResponseEntity<?> handleResourceNotFoundException(ResourceNotFoundException ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        response.put("message", ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.NOT_FOUND);
    }

    @ExceptionHandler(BadRequestException.class)
    public ResponseEntity<?> handleBadRequestException(BadRequestException ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        response.put("message", ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }

    @ExceptionHandler(MethodArgumentNotValidException.class)
    public ResponseEntity<?> handleValidationExceptions(MethodArgumentNotValidException ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        Map<String, String> errors = new HashMap<>();
        ex.getBindingResult().getFieldErrors().forEach(error -> 
            errors.put(error.getField(), error.getDefaultMessage())
        );
        response.put("message", "Validation Error");
        response.put("errors", errors);
        return new ResponseEntity<>(response, HttpStatus.BAD_REQUEST);
    }
    
    @ExceptionHandler(Exception.class)
    public ResponseEntity<?> handleGlobalException(Exception ex) {
        Map<String, Object> response = new HashMap<>();
        response.put("success", false);
        response.put("message", "An unexpected error occurred: " + ex.getMessage());
        return new ResponseEntity<>(response, HttpStatus.INTERNAL_SERVER_ERROR);
    }
}
""",
    "src/main/java/com/skillswap/exception/ResourceNotFoundException.java": """package com.skillswap.exception;
public class ResourceNotFoundException extends RuntimeException {
    public ResourceNotFoundException(String message) {
        super(message);
    }
}
""",
    "src/main/java/com/skillswap/exception/BadRequestException.java": """package com.skillswap.exception;
public class BadRequestException extends RuntimeException {
    public BadRequestException(String message) {
        super(message);
    }
}
""",

    # DTOS
    "src/main/java/com/skillswap/dto/LoginRequest.java": """package com.skillswap.dto;
import jakarta.validation.constraints.NotBlank;
public class LoginRequest {
    @NotBlank
    private String email;
    @NotBlank
    private String password;
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
}
""",
    "src/main/java/com/skillswap/dto/RegisterRequest.java": """package com.skillswap.dto;
import jakarta.validation.constraints.Email;
import jakarta.validation.constraints.NotBlank;
import java.util.Set;
public class RegisterRequest {
    @NotBlank
    private String name;
    @NotBlank
    @Email
    private String email;
    @NotBlank
    private String password;
    private String college;
    private String location;
    private String bio;
    private Set<String> skillsToTeach;
    private Set<String> skillsToLearn;
    
    // Getters and setters
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getPassword() { return password; }
    public void setPassword(String password) { this.password = password; }
    public String getCollege() { return college; }
    public void setCollege(String college) { this.college = college; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public String getBio() { return bio; }
    public void setBio(String bio) { this.bio = bio; }
    public Set<String> getSkillsToTeach() { return skillsToTeach; }
    public void setSkillsToTeach(Set<String> skillsToTeach) { this.skillsToTeach = skillsToTeach; }
    public Set<String> getSkillsToLearn() { return skillsToLearn; }
    public void setSkillsToLearn(Set<String> skillsToLearn) { this.skillsToLearn = skillsToLearn; }
}
""",
    "src/main/java/com/skillswap/dto/UserResponse.java": """package com.skillswap.dto;
import java.time.LocalDateTime;
import java.util.Set;
public class UserResponse {
    private Long id;
    private String name;
    private String email;
    private String college;
    private String location;
    private String bio;
    private String profileImage;
    private String availability;
    private Double rating;
    private Integer reviewCount;
    private Set<String> skillsToTeach;
    private Set<String> skillsToLearn;
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getEmail() { return email; }
    public void setEmail(String email) { this.email = email; }
    public String getCollege() { return college; }
    public void setCollege(String college) { this.college = college; }
    public String getLocation() { return location; }
    public void setLocation(String location) { this.location = location; }
    public String getBio() { return bio; }
    public void setBio(String bio) { this.bio = bio; }
    public String getProfileImage() { return profileImage; }
    public void setProfileImage(String profileImage) { this.profileImage = profileImage; }
    public String getAvailability() { return availability; }
    public void setAvailability(String availability) { this.availability = availability; }
    public Double getRating() { return rating; }
    public void setRating(Double rating) { this.rating = rating; }
    public Integer getReviewCount() { return reviewCount; }
    public void setReviewCount(Integer reviewCount) { this.reviewCount = reviewCount; }
    public Set<String> getSkillsToTeach() { return skillsToTeach; }
    public void setSkillsToTeach(Set<String> skillsToTeach) { this.skillsToTeach = skillsToTeach; }
    public Set<String> getSkillsToLearn() { return skillsToLearn; }
    public void setSkillsToLearn(Set<String> skillsToLearn) { this.skillsToLearn = skillsToLearn; }
}
""",
    "src/main/java/com/skillswap/dto/JwtResponse.java": """package com.skillswap.dto;
public class JwtResponse {
    private String token;
    private String type = "Bearer";
    private UserResponse user;
    
    public JwtResponse(String token, UserResponse user) {
        this.token = token;
        this.user = user;
    }
    public String getToken() { return token; }
    public void setToken(String token) { this.token = token; }
    public String getType() { return type; }
    public void setType(String type) { this.type = type; }
    public UserResponse getUser() { return user; }
    public void setUser(UserResponse user) { this.user = user; }
}
""",
    "src/main/java/com/skillswap/dto/ApiResponse.java": """package com.skillswap.dto;
public class ApiResponse {
    private boolean success;
    private String message;
    private Object data;
    
    public ApiResponse(boolean success, String message) {
        this.success = success;
        this.message = message;
    }
    public ApiResponse(boolean success, String message, Object data) {
        this.success = success;
        this.message = message;
        this.data = data;
    }
    // Getters and setters
    public boolean isSuccess() { return success; }
    public void setSuccess(boolean success) { this.success = success; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public Object getData() { return data; }
    public void setData(Object data) { this.data = data; }
}
""",
    "src/main/java/com/skillswap/dto/ExchangeRequestDTO.java": """package com.skillswap.dto;
import java.time.LocalDateTime;
public class ExchangeRequestDTO {
    private Long id;
    private Long fromUserId;
    private Long toUserId;
    private String fromUserName;
    private String toUserName;
    private String message;
    private String status;
    private LocalDateTime date;
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getFromUserId() { return fromUserId; }
    public void setFromUserId(Long fromUserId) { this.fromUserId = fromUserId; }
    public Long getToUserId() { return toUserId; }
    public void setToUserId(Long toUserId) { this.toUserId = toUserId; }
    public String getFromUserName() { return fromUserName; }
    public void setFromUserName(String fromUserName) { this.fromUserName = fromUserName; }
    public String getToUserName() { return toUserName; }
    public void setToUserName(String toUserName) { this.toUserName = toUserName; }
    public String getMessage() { return message; }
    public void setMessage(String message) { this.message = message; }
    public String getStatus() { return status; }
    public void setStatus(String status) { this.status = status; }
    public LocalDateTime getDate() { return date; }
    public void setDate(LocalDateTime date) { this.date = date; }
}
""",
    "src/main/java/com/skillswap/dto/ReviewDTO.java": """package com.skillswap.dto;
import jakarta.validation.constraints.Max;
import jakarta.validation.constraints.Min;
import jakarta.validation.constraints.NotBlank;
import jakarta.validation.constraints.NotNull;
import java.time.LocalDateTime;

public class ReviewDTO {
    private Long id;
    private Long fromUserId;
    @NotNull
    private Long toUserId;
    private String authorName;
    @Min(1) @Max(5)
    private Integer rating;
    @NotBlank
    private String text;
    private LocalDateTime date;
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getFromUserId() { return fromUserId; }
    public void setFromUserId(Long fromUserId) { this.fromUserId = fromUserId; }
    public Long getToUserId() { return toUserId; }
    public void setToUserId(Long toUserId) { this.toUserId = toUserId; }
    public String getAuthorName() { return authorName; }
    public void setAuthorName(String authorName) { this.authorName = authorName; }
    public Integer getRating() { return rating; }
    public void setRating(Integer rating) { this.rating = rating; }
    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
    public LocalDateTime getDate() { return date; }
    public void setDate(LocalDateTime date) { this.date = date; }
}
""",
    "src/main/java/com/skillswap/dto/MessageDTO.java": """package com.skillswap.dto;
import java.time.LocalDateTime;
public class MessageDTO {
    private Long id;
    private Long conversationId;
    private Long fromUserId;
    private Long toUserId;
    private String text;
    private LocalDateTime timestamp;
    private boolean isRead;
    
    // Getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public Long getConversationId() { return conversationId; }
    public void setConversationId(Long conversationId) { this.conversationId = conversationId; }
    public Long getFromUserId() { return fromUserId; }
    public void setFromUserId(Long fromUserId) { this.fromUserId = fromUserId; }
    public Long getToUserId() { return toUserId; }
    public void setToUserId(Long toUserId) { this.toUserId = toUserId; }
    public String getText() { return text; }
    public void setText(String text) { this.text = text; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
    public boolean getIsRead() { return isRead; }
    public void setIsRead(boolean isRead) { this.isRead = isRead; }
}
""",
    "src/main/java/com/skillswap/dto/ConversationDTO.java": """package com.skillswap.dto;
public class ConversationDTO {
    private Long id;
    private UserResponse otherUser;
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public UserResponse getOtherUser() { return otherUser; }
    public void setOtherUser(UserResponse otherUser) { this.otherUser = otherUser; }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
