package com.skillswap.controller;
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
