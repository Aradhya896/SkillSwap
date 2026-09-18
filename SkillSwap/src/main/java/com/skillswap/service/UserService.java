package com.skillswap.service;
import com.skillswap.dto.UserResponse;
import com.skillswap.entity.User;
import com.skillswap.exception.ResourceNotFoundException;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;\nimport com.skillswap.entity.Skill;\nimport java.util.Set;

@Service
public class UserService {
    @Autowired UserRepository userRepository;\n    @Autowired SkillService skillService;

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
        
        if (userDto.getSkillsToTeach() != null) {
            user.setSkillsToTeach(userDto.getSkillsToTeach().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }
        
        if (userDto.getSkillsToLearn() != null) {
            user.setSkillsToLearn(userDto.getSkillsToLearn().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }
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
        response.setSkillsToTeach(user.getSkillsToTeach().stream().map(Skill::getName).collect(Collectors.toSet()));
        response.setSkillsToLearn(user.getSkillsToLearn().stream().map(Skill::getName).collect(Collectors.toSet()));
        return response;
    }
}
