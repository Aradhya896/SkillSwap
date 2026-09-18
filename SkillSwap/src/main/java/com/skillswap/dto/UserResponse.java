package com.skillswap.dto;
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
