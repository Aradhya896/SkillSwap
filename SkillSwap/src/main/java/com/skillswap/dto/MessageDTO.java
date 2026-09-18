package com.skillswap.dto;
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
