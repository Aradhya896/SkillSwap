package com.skillswap.service;
import com.skillswap.dto.ConversationDTO;
import com.skillswap.dto.MessageDTO;
import com.skillswap.entity.Conversation;
import com.skillswap.entity.Message;
import com.skillswap.entity.User;
import com.skillswap.exception.ResourceNotFoundException;
import com.skillswap.repository.ConversationRepository;
import com.skillswap.repository.MessageRepository;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ChatService {
    @Autowired ConversationRepository conversationRepository;
    @Autowired MessageRepository messageRepository;
    @Autowired UserRepository userRepository;
    @Autowired UserService userService;

    public List<ConversationDTO> getUserConversations(Long userId) {
        return conversationRepository.findByUserId(userId).stream().map(c -> {
            ConversationDTO dto = new ConversationDTO();
            dto.setId(c.getId());
            User otherUser = c.getUserOne().getId().equals(userId) ? c.getUserTwo() : c.getUserOne();
            dto.setOtherUser(userService.mapToUserResponse(otherUser));
            return dto;
        }).collect(Collectors.toList());
    }

    public List<MessageDTO> getMessages(Long conversationId) {
        return messageRepository.findByConversationIdOrderByTimestampAsc(conversationId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    public MessageDTO sendMessage(Long senderId, MessageDTO dto) {
        User sender = userRepository.findById(senderId).orElseThrow();
        User receiver = userRepository.findById(dto.getToUserId()).orElseThrow();
        
        Conversation conversation = conversationRepository.findByUsers(senderId, dto.getToUserId())
            .orElseGet(() -> {
                Conversation c = new Conversation();
                c.setUserOne(sender);
                c.setUserTwo(receiver);
                return conversationRepository.save(c);
            });

        Message message = new Message();
        message.setConversation(conversation);
        message.setSender(sender);
        message.setMessage(dto.getText());
        messageRepository.save(message);
        return mapToDTO(message);
    }
    
    private MessageDTO mapToDTO(Message m) {
        MessageDTO dto = new MessageDTO();
        dto.setId(m.getId());
        dto.setConversationId(m.getConversation().getId());
        dto.setFromUserId(m.getSender().getId());
        dto.setToUserId(m.getConversation().getUserOne().getId().equals(m.getSender().getId()) ? 
            m.getConversation().getUserTwo().getId() : m.getConversation().getUserOne().getId());
        dto.setText(m.getMessage());
        dto.setTimestamp(m.getTimestamp());
        dto.setIsRead(m.getIsRead());
        return dto;
    }
}
