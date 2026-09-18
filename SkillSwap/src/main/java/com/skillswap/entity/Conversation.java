package com.skillswap.entity;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "conversations")
public class Conversation {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_one_id", nullable = false)
    private User userOne;

    @ManyToOne(fetch = FetchType.LAZY)
    @JoinColumn(name = "user_two_id", nullable = false)
    private User userTwo;

    @Column(updatable = false)
    private LocalDateTime createdAt = LocalDateTime.now();

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public User getUserOne() { return userOne; }
    public void setUserOne(User userOne) { this.userOne = userOne; }
    public User getUserTwo() { return userTwo; }
    public void setUserTwo(User userTwo) { this.userTwo = userTwo; }
    public LocalDateTime getCreatedAt() { return createdAt; }
    public void setCreatedAt(LocalDateTime createdAt) { this.createdAt = createdAt; }
}
