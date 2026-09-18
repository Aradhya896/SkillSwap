package com.skillswap.controller;
import com.skillswap.dto.ApiResponse;
import com.skillswap.dto.ExchangeRequestDTO;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.ExchangeRequestService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;
import java.util.Map;

@RestController
@RequestMapping("/api/requests")
public class ExchangeRequestController {
    @Autowired ExchangeRequestService requestService;

    @PostMapping
    public ResponseEntity<?> sendRequest(@RequestBody ExchangeRequestDTO requestDTO, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Request sent", requestService.createRequest(userDetails.getId(), requestDTO)));
    }

    @GetMapping("/incoming")
    public ResponseEntity<?> getIncomingRequests(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(requestService.getIncomingRequests(userDetails.getId()));
    }

    @GetMapping("/sent")
    public ResponseEntity<?> getSentRequests(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(requestService.getSentRequests(userDetails.getId()));
    }

    @PutMapping("/{id}/accept")
    public ResponseEntity<?> acceptRequest(@PathVariable Long id, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Request accepted", requestService.updateRequestStatus(id, userDetails.getId(), "accepted")));
    }

    @PutMapping("/{id}/reject")
    public ResponseEntity<?> rejectRequest(@PathVariable Long id, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(new ApiResponse(true, "Request rejected", requestService.updateRequestStatus(id, userDetails.getId(), "rejected")));
    }
}
