package com.skillswap.repository;
import com.skillswap.entity.ExchangeRequest;
import com.skillswap.entity.User;
import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.stereotype.Repository;
import java.util.List;
import java.util.Optional;

@Repository
public interface ExchangeRequestRepository extends JpaRepository<ExchangeRequest, Long> {
    List<ExchangeRequest> findBySenderId(Long senderId);
    List<ExchangeRequest> findByReceiverId(Long receiverId);
    Optional<ExchangeRequest> findBySenderAndReceiverAndStatus(User sender, User receiver, ExchangeRequest.RequestStatus status);
}
