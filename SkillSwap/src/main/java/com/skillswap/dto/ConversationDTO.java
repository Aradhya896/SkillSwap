package com.skillswap.dto;
public class ConversationDTO {
    private Long id;
    private UserResponse otherUser;
    
    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public UserResponse getOtherUser() { return otherUser; }
    public void setOtherUser(UserResponse otherUser) { this.otherUser = otherUser; }
}
