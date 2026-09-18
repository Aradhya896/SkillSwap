import os

files = {
    "src/main/java/com/skillswap/entity/Skill.java": """package com.skillswap.entity;

import jakarta.persistence.*;

@Entity
@Table(name = "skills")
public class Skill {
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    @Column(nullable = false, unique = true)
    private String name;

    private String category;

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getName() { return name; }
    public void setName(String name) { this.name = name; }
    public String getCategory() { return category; }
    public void setCategory(String category) { this.category = category; }
}
""",
    "src/main/java/com/skillswap/repository/SkillRepository.java": """package com.skillswap.repository;
import com.skillswap.entity.Skill;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.Optional;

@Repository
public interface SkillRepository extends JpaRepository<Skill, Long> {
    Optional<Skill> findByName(String name);
}
""",
    "src/main/java/com/skillswap/service/SkillService.java": """package com.skillswap.service;
import com.skillswap.entity.Skill;
import com.skillswap.repository.SkillRepository;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.stereotype.Service;
import java.util.List;

@Service
public class SkillService {
    @Autowired SkillRepository skillRepository;

    public List<Skill> getAllSkills() {
        return skillRepository.findAll();
    }

    public Skill getOrCreateSkill(String name, String category) {
        return skillRepository.findByName(name).orElseGet(() -> {
            Skill skill = new Skill();
            skill.setName(name);
            skill.setCategory(category);
            return skillRepository.save(skill);
        });
    }
}
""",
    "src/main/java/com/skillswap/controller/SkillController.java": """package com.skillswap.controller;
import com.skillswap.entity.Skill;
import com.skillswap.service.SkillService;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/skills")
public class SkillController {
    @Autowired SkillService skillService;

    @GetMapping
    public ResponseEntity<?> getAllSkills() {
        return ResponseEntity.ok(skillService.getAllSkills());
    }

    @PostMapping
    public ResponseEntity<?> createSkill(@RequestBody Skill skill) {
        return ResponseEntity.ok(skillService.getOrCreateSkill(skill.getName(), skill.getCategory()));
    }
}
"""
}

for path, content in files.items():
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w") as f:
        f.write(content)
