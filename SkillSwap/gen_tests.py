import os

files = {
    "src/test/java/com/skillswap/SkillSwapApplicationTests.java": """package com.skillswap;
import org.junit.jupiter.api.Test;
import org.springframework.boot.test.context.SpringBootTest;

@SpringBootTest
class SkillSwapApplicationTests {

    @Test
    void contextLoads() {
    }

}
""",
    "src/test/java/com/skillswap/service/AuthServiceTest.java": """package com.skillswap.service;
import com.skillswap.dto.RegisterRequest;
import com.skillswap.dto.UserResponse;
import com.skillswap.entity.User;
import com.skillswap.exception.BadRequestException;
import com.skillswap.repository.UserRepository;
import org.junit.jupiter.api.Test;
import org.junit.jupiter.api.extension.ExtendWith;
import org.mockito.InjectMocks;
import org.mockito.Mock;
import org.mockito.junit.jupiter.MockitoExtension;
import org.springframework.security.crypto.password.PasswordEncoder;
import java.util.HashSet;
import java.util.Optional;

import static org.junit.jupiter.api.Assertions.*;
import static org.mockito.ArgumentMatchers.any;
import static org.mockito.Mockito.when;

@ExtendWith(MockitoExtension.class)
public class AuthServiceTest {

    @Mock
    UserRepository userRepository;
    @Mock
    PasswordEncoder passwordEncoder;
    @Mock
    SkillService skillService;

    @InjectMocks
    AuthService authService;

    @Test
    public void registerUser_Valid_ReturnsUserResponse() {
        RegisterRequest req = new RegisterRequest();
        req.setEmail("test@test.com");
        req.setName("Test");
        req.setPassword("pass");
        req.setSkillsToTeach(new HashSet<>());
        req.setSkillsToLearn(new HashSet<>());
        
        when(userRepository.existsByEmail("test@test.com")).thenReturn(false);
        when(passwordEncoder.encode("pass")).thenReturn("encoded");
        when(userRepository.save(any(User.class))).thenAnswer(i -> i.getArguments()[0]);

        UserResponse res = authService.registerUser(req);
        assertNotNull(res);
        assertEquals("test@test.com", res.getEmail());
    }

    @Test
    public void registerUser_DuplicateEmail_ThrowsException() {
        RegisterRequest req = new RegisterRequest();
        req.setEmail("test@test.com");
        
        when(userRepository.existsByEmail("test@test.com")).thenReturn(true);
        
        assertThrows(BadRequestException.class, () -> authService.registerUser(req));
    }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
