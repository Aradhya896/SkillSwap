package com.skillswap.config;
import com.skillswap.entity.User;
import com.skillswap.repository.UserRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.CommandLineRunner;
import org.springframework.security.crypto.password.PasswordEncoder;
import org.springframework.stereotype.Component;
import java.util.Set;\nimport java.util.stream.Collectors;\nimport com.skillswap.service.SkillService;

@Component
public class DataInitializer implements CommandLineRunner {
    @Autowired UserRepository userRepository;
    @Autowired PasswordEncoder passwordEncoder;\n    @Autowired SkillService skillService;

    @Override
    public void run(String... args) throws Exception {
        if (userRepository.count() == 0) {
            String encodedPassword = passwordEncoder.encode("123456");

            User demo = new User();
            demo.setName("Demo User");
            demo.setEmail("demo@skillswap.com");
            demo.setPassword(encodedPassword);
            demo.setCollege("Pune University");
            demo.setLocation("Pune");
            demo.setBio("I am a demo user exploring the SkillSwap platform.");
            demo.setAvailability("Flexible");
            demo.setSkillsToTeach(Set.of("Photography", "Excel").stream().map(n -> skillService.getOrCreateSkill(n, "Other")).collect(Collectors.toSet()));
            demo.setSkillsToLearn(Set.of("Java", "Public Speaking").stream().map(n -> skillService.getOrCreateSkill(n, "Other")).collect(Collectors.toSet()));
            demo.setRating(5.0);
            demo.setReviewCount(1);
            userRepository.save(demo);

            User user1 = new User();
            user1.setName("Aarav Sharma");
            user1.setEmail("aarav@example.com");
            user1.setPassword(encodedPassword);
            user1.setCollege("Galgotias University");
            user1.setLocation("Greater Noida");
            user1.setBio("Computer science student interested in web development.");
            user1.setAvailability("Weekends");
            user1.setSkillsToTeach(Set.of("Java", "HTML", "CSS").stream().map(n -> skillService.getOrCreateSkill(n, "Other")).collect(Collectors.toSet()));
            user1.setSkillsToLearn(Set.of("Python", "Machine Learning").stream().map(n -> skillService.getOrCreateSkill(n, "Other")).collect(Collectors.toSet()));
            user1.setRating(4.7);
            user1.setReviewCount(5);
            userRepository.save(user1);

            User user2 = new User();
            user2.setName("Priya Patel");
            user2.setEmail("priya@example.com");
            user2.setPassword(encodedPassword);
            user2.setCollege("IIT Bombay");
            user2.setLocation("Mumbai");
            user2.setBio("UI/UX Designer who loves creating beautiful interfaces.");
            user2.setAvailability("Evenings");
            user2.setSkillsToTeach(Set.of("UI/UX", "Figma", "Design").stream().map(n -> skillService.getOrCreateSkill(n, "Other")).collect(Collectors.toSet()));
            user2.setSkillsToLearn(Set.of("JavaScript", "React").stream().map(n -> skillService.getOrCreateSkill(n, "Other")).collect(Collectors.toSet()));
            user2.setRating(4.9);
            user2.setReviewCount(10);
            userRepository.save(user2);
            
            System.out.println("Sample data initialized!");
        }
    }
}
