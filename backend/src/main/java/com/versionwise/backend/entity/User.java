
package com.versionwise.backend.entity;

import jakarta.persistence.Column;
import jakarta.persistence.Entity;
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;
import jakarta.persistence.Table;

import java.time.Instant;
import java.util.UUID;

@Entity
@Table(name = "app_users")
public class User {

    @Id
    @GeneratedValue(strategy = GenerationType.UUID)
    private UUID id;

    @Column(nullable = false, unique = true, length = 254)
    private String email;

    public String getPasswordHash() {
        return passwordHash;
    }


    @Column(name = "password_hash", length = 100)
    private String passwordHash;

    @Column(nullable = false, updatable = false)
    private Instant createdAt;

    protected User() {
        // Required by JPA
    }

    public User(String email) {
        this.email = email.trim().toLowerCase(java.util.Locale.ROOT);
        this.createdAt = Instant.now();
    }
    public User(String email, String passwordHash) {
        this.email = email.trim().toLowerCase(java.util.Locale.ROOT);
        this.passwordHash = passwordHash;
        this.createdAt = Instant.now();
    }

    public UUID getId() {
        return id;
    }

    public String getEmail() {
        return email;
    }

    public Instant getCreatedAt() {
        return createdAt;
    }
}
