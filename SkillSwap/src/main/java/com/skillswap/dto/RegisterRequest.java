package com.skillswap.dto;
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
