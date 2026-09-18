package com.skillswap.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;
import java.util.HashSet;
import java.util.Set;

@Entity
@Table(name = "users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false)
    private String name;

    @Column(nullable = false, unique = true)
    private String email;

    @Column(nullable = false)
    private String password;

    private String college;
    private String location;
    
    @Column(columnDefinition = "TEXT")
    private String bio;
    
    private String profileImage;
    private String availability;
    
    private Double rating = 0.0;
    private Integer reviewCount = 0;
    
    @Column(updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "user_teach_skills",
            joinColumns = @JoinColumn(name = "user_id"),
            inverseJoinColumns = @JoinColumn(name = "skill_id"))
    private Set<Skill> skillsToTeach = new HashSet<>();

    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "user_learn_skills",
            joinColumns = @JoinColumn(name = "user_id"),
            inverseJoinColumns = @JoinColumn(name = "skill_id"))
    private Set<Skill> skillsToLearn = new HashSet<>();

    // Standard getters and setters
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
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
    public String getProfileImage() { return profileImage; }
    public void setProfileImage(String profileImage) { this.profileImage = profileImage; }
    public String getAvailability() { return availability; }
    public void setAvailability(String availability) { this.availability = availability; }
    public Double getRating() { return rating; }
    public void setRating(Double rating) { this.rating = rating; }
    public Integer getReviewCount() { return reviewCount; }
    public void setReviewCount(Integer reviewCount) { this.reviewCount = reviewCount; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
    public Set<Skill> getSkillsToTeach() { return skillsToTeach; }
    public void setSkillsToTeach(Set<Skill> skillsToTeach) { this.skillsToTeach = skillsToTeach; }
    public Set<Skill> getSkillsToLearn() { return skillsToLearn; }
    public void setSkillsToLearn(Set<Skill> skillsToLearn) { this.skillsToLearn = skillsToLearn; }
}
