package com.skillswap.service;
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
