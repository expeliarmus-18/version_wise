
package com.versionwise.backend.controller;

import com.versionwise.backend.auth.AuthService;
import com.versionwise.backend.auth.dto.AuthResponse;
import com.versionwise.backend.auth.dto.LoginRequest;
import com.versionwise.backend.auth.dto.RegisterRequest;
import com.versionwise.backend.auth.dto.UserResponse;

import jakarta.validation.Valid;

import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.*;

@RestController
@RequestMapping("/api/auth")
public class AuthController {

    private final AuthService authService;

    public AuthController(AuthService authService) {
        this.authService = authService;
    }

    @PostMapping("/register")
    @ResponseStatus(HttpStatus.CREATED)
    public UserResponse register(
            @Valid @RequestBody RegisterRequest request) {
        return authService.register(request);
    }

    @PostMapping("/login")
    public AuthResponse login(
            @Valid @RequestBody LoginRequest request) {
        return authService.login(request);
    }
}
