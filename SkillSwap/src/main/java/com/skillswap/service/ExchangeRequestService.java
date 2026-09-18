package com.skillswap.service;
import com.skillswap.dto.ExchangeRequestDTO;
import com.skillswap.entity.ExchangeRequest;
import com.skillswap.entity.User;
import com.skillswap.exception.BadRequestException;
import com.skillswap.exception.ResourceNotFoundException;
import com.skillswap.repository.ExchangeRequestRepository;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;
import java.util.stream.Collectors;

@Service
public class ExchangeRequestService {
    @Autowired ExchangeRequestRepository requestRepository;
    @Autowired UserRepository userRepository;

    public ExchangeRequestDTO createRequest(Long senderId, ExchangeRequestDTO dto) {
        if (senderId.equals(dto.getToUserId())) throw new BadRequestException("Cannot send request to yourself");
        
        User sender = userRepository.findById(senderId).orElseThrow(() -> new ResourceNotFoundException("Sender not found"));
        User receiver = userRepository.findById(dto.getToUserId()).orElseThrow(() -> new ResourceNotFoundException("Receiver not found"));

        if (requestRepository.findBySenderAndReceiverAndStatus(sender, receiver, ExchangeRequest.RequestStatus.PENDING).isPresent()) {
            throw new BadRequestException("Pending request already exists");
        }

        ExchangeRequest request = new ExchangeRequest();
        request.setSender(sender);
        request.setReceiver(receiver);
        request.setMessage(dto.getMessage());
        request.setStatus(ExchangeRequest.RequestStatus.PENDING);
        requestRepository.save(request);
        return mapToDTO(request);
    }

    public List<ExchangeRequestDTO> getIncomingRequests(Long userId) {
        return requestRepository.findByReceiverId(userId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    public List<ExchangeRequestDTO> getSentRequests(Long userId) {
        return requestRepository.findBySenderId(userId).stream().map(this::mapToDTO).collect(Collectors.toList());
    }

    public ExchangeRequestDTO updateRequestStatus(Long requestId, Long userId, String status) {
        ExchangeRequest request = requestRepository.findById(requestId).orElseThrow(() -> new ResourceNotFoundException("Request not found"));
        if (!request.getReceiver().getId().equals(userId)) {
            throw new BadRequestException("Unauthorized to update this request");
        }
        if ("accepted".equalsIgnoreCase(status)) request.setStatus(ExchangeRequest.RequestStatus.ACCEPTED);
        else if ("rejected".equalsIgnoreCase(status)) request.setStatus(ExchangeRequest.RequestStatus.REJECTED);
        else throw new BadRequestException("Invalid status");
        
        requestRepository.save(request);
        return mapToDTO(request);
    }

    private ExchangeRequestDTO mapToDTO(ExchangeRequest req) {
        ExchangeRequestDTO dto = new ExchangeRequestDTO();
        dto.setId(req.getId());
        dto.setFromUserId(req.getSender().getId());
        dto.setToUserId(req.getReceiver().getId());
        dto.setFromUserName(req.getSender().getName());
        dto.setToUserName(req.getReceiver().getName());
        dto.setMessage(req.getMessage());
        dto.setStatus(req.getStatus().name().toLowerCase());
        dto.setDate(req.getCreatedAt());
        return dto;
    }
}
