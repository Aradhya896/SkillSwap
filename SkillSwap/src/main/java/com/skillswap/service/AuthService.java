package com.skillswap.service;
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
import org.springframework.stereotype.Service;\nimport java.util.stream.Collectors;\nimport com.skillswap.entity.Skill;\nimport java.util.Set;

@Service
public class AuthService {
    @Autowired AuthenticationManager authenticationManager;
    @Autowired UserRepository userRepository;
    @Autowired PasswordEncoder encoder;
    @Autowired JwtUtils jwtUtils;\n    @Autowired SkillService skillService;

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
        
        if (signUpRequest.getSkillsToTeach() != null) {
            user.setSkillsToTeach(signUpRequest.getSkillsToTeach().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }
        
        if (signUpRequest.getSkillsToLearn() != null) {
            user.setSkillsToLearn(signUpRequest.getSkillsToLearn().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }
        
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
        response.setSkillsToTeach(user.getSkillsToTeach().stream().map(Skill::getName).collect(Collectors.toSet()));
        response.setSkillsToLearn(user.getSkillsToLearn().stream().map(Skill::getName).collect(Collectors.toSet()));
        return response;
    }
}
