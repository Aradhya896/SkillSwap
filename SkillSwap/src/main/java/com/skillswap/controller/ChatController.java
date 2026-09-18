package com.skillswap.controller;
import com.skillswap.dto.MessageDTO;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.ChatService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/conversations")
public class ChatController {
    @Autowired ChatService chatService;

    @GetMapping
    public ResponseEntity<?> getUserConversations(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(chatService.getUserConversations(userDetails.getId()));
    }

    @GetMapping("/{id}/messages")
    public ResponseEntity<?> getMessages(@PathVariable Long id) {
        return ResponseEntity.ok(chatService.getMessages(id));
    }

    @PostMapping("/{id}/messages")
    public ResponseEntity<?> sendMessage(@PathVariable Long id, @RequestBody MessageDTO messageDTO, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        // Here ID is conversation ID, but the service creates or finds conversation based on toUserId 
        // to simplify the flow as per the frontend implementation.
        return ResponseEntity.ok(chatService.sendMessage(userDetails.getId(), messageDTO));
    }
}
