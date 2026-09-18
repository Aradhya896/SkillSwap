import os

user_java_path = "src/main/java/com/skillswap/entity/User.java"
with open(user_java_path, "r") as f:
    user_code = f.read()

# Replace ElementCollection with ManyToMany
old_teach = """    @ElementCollection
    @CollectionTable(name = "user_teach_skills", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "skill_name")
    private Set<String> skillsToTeach = new HashSet<>();"""

new_teach = """    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "user_teach_skills",
            joinColumns = @JoinColumn(name = "user_id"),
            inverseJoinColumns = @JoinColumn(name = "skill_id"))
    private Set<Skill> skillsToTeach = new HashSet<>();"""

old_learn = """    @ElementCollection
    @CollectionTable(name = "user_learn_skills", joinColumns = @JoinColumn(name = "user_id"))
    @Column(name = "skill_name")
    private Set<String> skillsToLearn = new HashSet<>();"""

new_learn = """    @ManyToMany(fetch = FetchType.LAZY)
    @JoinTable(name = "user_learn_skills",
            joinColumns = @JoinColumn(name = "user_id"),
            inverseJoinColumns = @JoinColumn(name = "skill_id"))
    private Set<Skill> skillsToLearn = new HashSet<>();"""

user_code = user_code.replace(old_teach, new_teach).replace(old_learn, new_learn)
# Also change getters and setters
user_code = user_code.replace("public Set<String> getSkillsToTeach()", "public Set<Skill> getSkillsToTeach()")
user_code = user_code.replace("public void setSkillsToTeach(Set<String> skillsToTeach)", "public void setSkillsToTeach(Set<Skill> skillsToTeach)")
user_code = user_code.replace("public Set<String> getSkillsToLearn()", "public Set<Skill> getSkillsToLearn()")
user_code = user_code.replace("public void setSkillsToLearn(Set<String> skillsToLearn)", "public void setSkillsToLearn(Set<Skill> skillsToLearn)")

with open(user_java_path, "w") as f:
    f.write(user_code)


auth_service_path = "src/main/java/com/skillswap/service/AuthService.java"
with open(auth_service_path, "r") as f:
    auth_code = f.read()

# Replace skill mapping in AuthService
auth_code = auth_code.replace("import org.springframework.stereotype.Service;", "import org.springframework.stereotype.Service;\\nimport java.util.stream.Collectors;\\nimport com.skillswap.entity.Skill;\\nimport java.util.Set;")

auth_code = auth_code.replace("user.setSkillsToTeach(signUpRequest.getSkillsToTeach());", """
        if (signUpRequest.getSkillsToTeach() != null) {
            user.setSkillsToTeach(signUpRequest.getSkillsToTeach().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }""")
auth_code = auth_code.replace("user.setSkillsToLearn(signUpRequest.getSkillsToLearn());", """
        if (signUpRequest.getSkillsToLearn() != null) {
            user.setSkillsToLearn(signUpRequest.getSkillsToLearn().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }""")
auth_code = auth_code.replace("response.setSkillsToTeach(user.getSkillsToTeach());", "response.setSkillsToTeach(user.getSkillsToTeach().stream().map(Skill::getName).collect(Collectors.toSet()));")
auth_code = auth_code.replace("response.setSkillsToLearn(user.getSkillsToLearn());", "response.setSkillsToLearn(user.getSkillsToLearn().stream().map(Skill::getName).collect(Collectors.toSet()));")
auth_code = auth_code.replace("@Autowired JwtUtils jwtUtils;", "@Autowired JwtUtils jwtUtils;\\n    @Autowired SkillService skillService;")

with open(auth_service_path, "w") as f:
    f.write(auth_code)

user_service_path = "src/main/java/com/skillswap/service/UserService.java"
with open(user_service_path, "r") as f:
    user_code_srv = f.read()

user_code_srv = user_code_srv.replace("import java.util.stream.Collectors;", "import java.util.stream.Collectors;\\nimport com.skillswap.entity.Skill;\\nimport java.util.Set;")
user_code_srv = user_code_srv.replace("@Autowired UserRepository userRepository;", "@Autowired UserRepository userRepository;\\n    @Autowired SkillService skillService;")

user_code_srv = user_code_srv.replace("user.setSkillsToTeach(userDto.getSkillsToTeach());", """
        if (userDto.getSkillsToTeach() != null) {
            user.setSkillsToTeach(userDto.getSkillsToTeach().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }""")
user_code_srv = user_code_srv.replace("user.setSkillsToLearn(userDto.getSkillsToLearn());", """
        if (userDto.getSkillsToLearn() != null) {
            user.setSkillsToLearn(userDto.getSkillsToLearn().stream()
                .map(name -> skillService.getOrCreateSkill(name, "Other"))
                .collect(Collectors.toSet()));
        }""")

user_code_srv = user_code_srv.replace("response.setSkillsToTeach(user.getSkillsToTeach());", "response.setSkillsToTeach(user.getSkillsToTeach().stream().map(Skill::getName).collect(Collectors.toSet()));")
user_code_srv = user_code_srv.replace("response.setSkillsToLearn(user.getSkillsToLearn());", "response.setSkillsToLearn(user.getSkillsToLearn().stream().map(Skill::getName).collect(Collectors.toSet()));")

with open(user_service_path, "w") as f:
    f.write(user_code_srv)

user_repo_path = "src/main/java/com/skillswap/repository/UserRepository.java"
with open(user_repo_path, "r") as f:
    user_repo = f.read()

user_repo = user_repo.replace("OR LOWER(t) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(l) LIKE LOWER(CONCAT('%', :search, '%'))", "OR LOWER(t.name) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(l.name) LIKE LOWER(CONCAT('%', :search, '%'))")

with open(user_repo_path, "w") as f:
    f.write(user_repo)

data_init_path = "src/main/java/com/skillswap/config/DataInitializer.java"
with open(data_init_path, "r") as f:
    data_init = f.read()

data_init = data_init.replace("import java.util.Set;", "import java.util.Set;\\nimport java.util.stream.Collectors;\\nimport com.skillswap.service.SkillService;")
data_init = data_init.replace("@Autowired PasswordEncoder passwordEncoder;", "@Autowired PasswordEncoder passwordEncoder;\\n    @Autowired SkillService skillService;")
data_init = data_init.replace("demo.setSkillsToTeach(Set.of(", "demo.setSkillsToTeach(Set.of(").replace("Set.of(", "Set.of(").replace("demo.setSkillsToTeach(Set.of(\"Photography\", \"Excel\"));", "demo.setSkillsToTeach(Set.of(\"Photography\", \"Excel\").stream().map(n -> skillService.getOrCreateSkill(n, \"Other\")).collect(Collectors.toSet()));")
data_init = data_init.replace("demo.setSkillsToLearn(Set.of(\"Java\", \"Public Speaking\"));", "demo.setSkillsToLearn(Set.of(\"Java\", \"Public Speaking\").stream().map(n -> skillService.getOrCreateSkill(n, \"Other\")).collect(Collectors.toSet()));")
data_init = data_init.replace("user1.setSkillsToTeach(Set.of(\"Java\", \"HTML\", \"CSS\"));", "user1.setSkillsToTeach(Set.of(\"Java\", \"HTML\", \"CSS\").stream().map(n -> skillService.getOrCreateSkill(n, \"Other\")).collect(Collectors.toSet()));")
data_init = data_init.replace("user1.setSkillsToLearn(Set.of(\"Python\", \"Machine Learning\"));", "user1.setSkillsToLearn(Set.of(\"Python\", \"Machine Learning\").stream().map(n -> skillService.getOrCreateSkill(n, \"Other\")).collect(Collectors.toSet()));")
data_init = data_init.replace("user2.setSkillsToTeach(Set.of(\"UI/UX\", \"Figma\", \"Design\"));", "user2.setSkillsToTeach(Set.of(\"UI/UX\", \"Figma\", \"Design\").stream().map(n -> skillService.getOrCreateSkill(n, \"Other\")).collect(Collectors.toSet()));")
data_init = data_init.replace("user2.setSkillsToLearn(Set.of(\"JavaScript\", \"React\"));", "user2.setSkillsToLearn(Set.of(\"JavaScript\", \"React\").stream().map(n -> skillService.getOrCreateSkill(n, \"Other\")).collect(Collectors.toSet()));")

with open(data_init_path, "w") as f:
    f.write(data_init)
