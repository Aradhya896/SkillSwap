import os

files = {
    # SERVICES
    "src/main/java/com/skillswap/service/AuthService.java": """package com.skillswap.service;
import com.skillswap.dto.JwtResponse;
import com.skillswap.dto.LoginRequest;
import com.skillswap.dto.RegisterRequest;
import com.skillswap.dto.UserResponse;
import com.skillswap.entity.User;
import com.skillswap.exception.BadRequestException;
import com.skillswap.repository.UserRepository;
import com.skillswap.security.JwtUtils;
import com.skillswap.security.UserDetailsImpl;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.security.authentication.AuthenticationManager;
import org.springframework.security.authentication.UsernamePasswordAuthenticationToken;
import org.springframework.security.core.Authentication;
import org.springframework.security.core.context.SecurityContextHolder;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Service;

@Service
public class AuthService {
    @Autowired AuthenticationManager authenticationManager;
    @Autowired UserRepository userRepository;
    @Autowired PasswordEncoder encoder;
    @Autowired JwtUtils jwtUtils;

    public JwtResponse authenticateUser(LoginRequest loginRequest) {
        Authentication authentication = authenticationManager.authenticate(
                new UsernamePasswordAuthenticationToken(loginRequest.getEmail(), loginRequest.getPassword()));
        SecurityContextHolder.getContext().setAuthentication(authentication);
        String jwt = jwtUtils.generateJwtToken(authentication);
        
        UserDetailsImpl userDetails = (UserDetailsImpl) authentication.getPrincipal();
        User user = userRepository.findById(userDetails.getId()).get();
        return new JwtResponse(jwt, mapToUserResponse(user));
    }

    public UserResponse registerUser(RegisterRequest signUpRequest) {
        if (userRepository.existsByEmail(signUpRequest.getEmail())) {
            throw new BadRequestException("Error: Email is already in use!");
        }
        User user = new User();
        user.setName(signUpRequest.getName());
        user.setEmail(signUpRequest.getEmail());
        user.setPassword(encoder.encode(signUpRequest.getPassword()));
        user.setCollege(signUpRequest.getCollege());
        user.setLocation(signUpRequest.getLocation());
        user.setBio(signUpRequest.getBio());
        user.setSkillsToTeach(signUpRequest.getSkillsToTeach());
        user.setSkillsToLearn(signUpRequest.getSkillsToLearn());
        
        userRepository.save(user);
        return mapToUserResponse(user);
    }
    
    private UserResponse mapToUserResponse(User user) {
        UserResponse response = new UserResponse();
        response.setId(user.getId());
        response.setName(user.getName());
        response.setEmail(user.getEmail());
        response.setCollege(user.getCollege());
        response.setLocation(user.getLocation());
        response.setBio(user.getBio());
        response.setProfileImage(user.getProfileImage());
        response.setAvailability(user.getAvailability());
        response.setRating(user.getRating());
        response.setReviewCount(user.getReviewCount());
        response.setSkillsToTeach(user.getSkillsToTeach());
        response.setSkillsToLearn(user.getSkillsToLearn());
        return response;
    }
}
""",
    "src/main/java/com/skillswap/service/UserService.java": """package com.skillswap.service;
import com.skillswap.dto.UserResponse;
import com.skillswap.entity.User;
import com.skillswap.exception.ResourceNotFoundException;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class UserService {
    @Autowired UserRepository userRepository;

    public List<UserResponse> searchUsers(String search, String location, Double minRating) {
        List<User> users = userRepository.searchUsers(search, location, minRating);
        return users.stream().map(this::mapToUserResponse).collect(Collectors.toList());
    }
    
    public List<UserResponse> getAllUsers() {
        return userRepository.findAll().stream().map(this::mapToUserResponse).collect(Collectors.toList());
    }

    public UserResponse getUserById(Long id) {
        User user = userRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("User not found"));
        return mapToUserResponse(user);
    }

    public UserResponse updateUser(Long id, UserResponse userDto) {
        User user = userRepository.findById(id).orElseThrow(() -> new ResourceNotFoundException("User not found"));
        user.setName(userDto.getName());
        user.setLocation(userDto.getLocation());
        user.setCollege(userDto.getCollege());
        user.setBio(userDto.getBio());
        user.setAvailability(userDto.getAvailability());
        user.setSkillsToTeach(userDto.getSkillsToTeach());
        user.setSkillsToLearn(userDto.getSkillsToLearn());
        userRepository.save(user);
        return mapToUserResponse(user);
    }

    public UserResponse mapToUserResponse(User user) {
        UserResponse response = new UserResponse();
        response.setId(user.getId());
        response.setName(user.getName());
        response.setEmail(user.getEmail());
        response.setCollege(user.getCollege());
        response.setLocation(user.getLocation());
        response.setBio(user.getBio());
        response.setProfileImage(user.getProfileImage());
        response.setAvailability(user.getAvailability());
        response.setRating(user.getRating());
        response.setReviewCount(user.getReviewCount());
        response.setSkillsToTeach(user.getSkillsToTeach());
        response.setSkillsToLearn(user.getSkillsToLearn());
        return response;
    }
}
""",
    "src/main/java/com/skillswap/service/ExchangeRequestService.java": """package com.skillswap.service;
import com.skillswap.dto.ExchangeRequestDTO;
import com.skillswap.entity.ExchangeRequest;
import com.skillswap.entity.User;
import com.skillswap.exception.BadRequestException;
import com.skillswap.exception.ResourceNotFoundException;
import com.skillswap.repository.ExchangeRequestRepository;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ExchangeRequestService {
    @Autowired ExchangeRequestRepository requestRepository;
    @Autowired UserRepository userRepository;

    public ExchangeRequestDTO createRequest(Long senderId, ExchangeRequestDTO dto) {
        if (senderId.equals(dto.getToUserId())) throw new BadRequestException("Cannot send request to yourself");
        
        User sender = userRepository.findById(senderId).orElseThrow(() -> new ResourceNotFoundException("Sender not found"));
        User receiver = userRepository.findById(dto.getToUserId()).orElseThrow(() -> new ResourceNotFoundException("Receiver not found"));

        if (requestRepository.findBySenderAndReceiverAndStatus(sender, receiver, ExchangeRequest.RequestStatus.PENDING).isPresent()) {
            throw new BadRequestException("Pending request already exists");
        }

        ExchangeRequest request = new ExchangeRequest();
        request.setSender(sender);
        request.setReceiver(receiver);
        request.setMessage(dto.getMessage());
        request.setStatus(ExchangeRequest.RequestStatus.PENDING);
        requestRepository.save(request);
        return mapToDTO(request);
    }

    public List<ExchangeRequestDTO> getIncomingRequests(Long userId) {
        return requestRepository.findByReceiverId(userId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    public List<ExchangeRequestDTO> getSentRequests(Long userId) {
        return requestRepository.findBySenderId(userId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    public ExchangeRequestDTO updateRequestStatus(Long requestId, Long userId, String status) {
        ExchangeRequest request = requestRepository.findById(requestId).orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        if (!request.getReceiver().getId().equals(userId)) {
            throw new BadRequestException("Unauthorized to update this request");
        }
        if ("accepted".equalsIgnoreCase(status)) request.setStatus(ExchangeRequest.RequestStatus.ACCEPTED);
        else if ("rejected".equalsIgnoreCase(status)) request.setStatus(ExchangeRequest.RequestStatus.REJECTED);
        else throw new BadRequestException("Invalid status");
        
        requestRepository.save(request);
        return mapToDTO(request);
    }

    private ExchangeRequestDTO mapToDTO(ExchangeRequest req) {
        ExchangeRequestDTO dto = new ExchangeRequestDTO();
        dto.setId(req.getId());
        dto.setFromUserId(req.getSender().getId());
        dto.setToUserId(req.getReceiver().getId());
        dto.setFromUserName(req.getSender().getName());
        dto.setToUserName(req.getReceiver().getName());
        dto.setMessage(req.getMessage());
        dto.setStatus(req.getStatus().name().toLowerCase());
        dto.setDate(req.getCreatedAt());
        return dto;
    }
}
""",
    "src/main/java/com/skillswap/service/ChatService.java": """package com.skillswap.service;
import com.skillswap.dto.ConversationDTO;
import com.skillswap.dto.MessageDTO;
import com.skillswap.entity.Conversation;
import com.skillswap.entity.Message;
import com.skillswap.entity.User;
import com.skillswap.exception.ResourceNotFoundException;
import com.skillswap.repository.ConversationRepository;
import com.skillswap.repository.MessageRepository;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ChatService {
    @Autowired ConversationRepository conversationRepository;
    @Autowired MessageRepository messageRepository;
    @Autowired UserRepository userRepository;
    @Autowired UserService userService;

    public List<ConversationDTO> getUserConversations(Long userId) {
        return conversationRepository.findByUserId(userId).stream().map(c -> {
            ConversationDTO dto = new ConversationDTO();
            dto.setId(c.getId());
            User otherUser = c.getUserOne().getId().equals(userId) ? c.getUserTwo() : c.getUserOne();
            dto.setOtherUser(userService.mapToUserResponse(otherUser));
            return dto;
        }).collect(Collectors.toList());
    }

    public List<MessageDTO> getMessages(Long conversationId) {
        return messageRepository.findByConversationIdOrderByTimestampAsc(conversationId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    public MessageDTO sendMessage(Long senderId, MessageDTO dto) {
        User sender = userRepository.findById(senderId).orElseThrow();
        User receiver = userRepository.findById(dto.getToUserId()).orElseThrow();
        
        Conversation conversation = conversationRepository.findByUsers(senderId, dto.getToUserId())
            .orElseGet(() -> {
                Conversation c = new Conversation();
                c.setUserOne(sender);
                c.setUserTwo(receiver);
                return conversationRepository.save(c);
            });

        Message message = new Message();
        message.setConversation(conversation);
        message.setSender(sender);
        message.setMessage(dto.getText());
        messageRepository.save(message);
        return mapToDTO(message);
    }
    
    private MessageDTO mapToDTO(Message m) {
        MessageDTO dto = new MessageDTO();
        dto.setId(m.getId());
        dto.setConversationId(m.getConversation().getId());
        dto.setFromUserId(m.getSender().getId());
        dto.setToUserId(m.getConversation().getUserOne().getId().equals(m.getSender().getId()) ? 
            m.getConversation().getUserTwo().getId() : m.getConversation().getUserOne().getId());
        dto.setText(m.getMessage());
        dto.setTimestamp(m.getTimestamp());
        dto.setIsRead(m.getIsRead());
        return dto;
    }
}
""",
    "src/main/java/com/skillswap/service/ReviewService.java": """package com.skillswap.service;
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
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
