package com.skillswap.dto;
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
