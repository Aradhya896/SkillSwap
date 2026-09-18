package com.skillswap.controller;
import com.skillswap.dto.ApiResponse;
import com.skillswap.dto.UserResponse;
import com.skillswap.security.UserDetailsImpl;
import com.skillswap.service.UserService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/users")
public class UserController {
    @Autowired UserService userService;

    @GetMapping
    public ResponseEntity<?> searchUsers(
            @RequestParam(required = false) String search,
            @RequestParam(required = false) String location,
            @RequestParam(required = false) Double minRating) {
        if (search == null && location == null && minRating == null) {
            return ResponseEntity.ok(userService.getAllUsers());
        }
        return ResponseEntity.ok(userService.searchUsers(search, location, minRating));
    }

    @GetMapping("/nearby")
    public ResponseEntity<?> getNearbyUsers(@RequestParam String location) {
        return ResponseEntity.ok(userService.searchUsers(null, location, null));
    }

    @GetMapping("/me")
    public ResponseEntity<?> getCurrentUser(@AuthenticationPrincipal UserDetailsImpl userDetails) {
        return ResponseEntity.ok(userService.getUserById(userDetails.getId()));
    }

    @GetMapping("/{id}")
    public ResponseEntity<?> getUserById(@PathVariable Long id) {
        return ResponseEntity.ok(userService.getUserById(id));
    }

    @PutMapping("/{id}")
    public ResponseEntity<?> updateUser(@PathVariable Long id, @RequestBody UserResponse userDto, @AuthenticationPrincipal UserDetailsImpl userDetails) {
        if (!id.equals(userDetails.getId())) return ResponseEntity.status(403).body(new ApiResponse(false, "Unauthorized"));
        return ResponseEntity.ok(new ApiResponse(true, "Profile updated", userService.updateUser(id, userDto)));
    }
}
