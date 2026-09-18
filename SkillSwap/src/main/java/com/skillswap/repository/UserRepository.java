package com.skillswap.repository;
import com.skillswap.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.jpa.repository.Query;
import org.springframework.data.repository.query.Param;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface UserRepository extends JpaRepository<User, Long> {
    Optional<User> findByEmail(String email);
    Boolean existsByEmail(String email);
    
    @Query("SELECT DISTINCT u FROM User u LEFT JOIN u.skillsToTeach t LEFT JOIN u.skillsToLearn l WHERE " +
           "(:search IS NULL OR LOWER(u.name) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(u.location) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(t.name) LIKE LOWER(CONCAT('%', :search, '%')) OR LOWER(l.name) LIKE LOWER(CONCAT('%', :search, '%'))) AND " +
           "(:location IS NULL OR LOWER(u.location) LIKE LOWER(CONCAT('%', :location, '%'))) AND " +
           "(:minRating IS NULL OR u.rating >= :minRating)")
    List<User> searchUsers(@Param("search") String search, @Param("location") String location, @Param("minRating") Double minRating);
}
