
package com.versionwise.backend;

import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.delete;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.get;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.post;
import static org.springframework.test.web.servlet.request.MockMvcRequestBuilders.put;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.jsonPath;
import static org.springframework.test.web.servlet.result.MockMvcResultMatchers.status;

import java.time.Instant;
import java.util.UUID;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.versionwise.backend.repository.ProjectRepository;
import com.versionwise.backend.repository.UserRepository;

import org.junit.jupiter.api.BeforeEach;
import org.junit.jupiter.api.Test;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.boot.test.autoconfigure.web.servlet.AutoConfigureMockMvc;
import org.springframework.boot.test.context.SpringBootTest;
import org.springframework.http.MediaType;
import org.springframework.security.oauth2.jose.jws.MacAlgorithm;
import org.springframework.security.oauth2.jwt.JwtClaimsSet;
import org.springframework.security.oauth2.jwt.JwtEncoder;
import org.springframework.security.oauth2.jwt.JwtEncoderParameters;
import org.springframework.security.oauth2.jwt.JwsHeader;
import org.springframework.test.web.servlet.MockMvc;
import org.springframework.test.web.servlet.MvcResult;

@SpringBootTest(properties = {
        "app.security.jwt-secret=versionwise-test-only-secret-not-for-production-123456789"
})
@AutoConfigureMockMvc
class SecurityIntegrationTests {

    @Autowired
    private MockMvc mockMvc;

    @Autowired
    private ObjectMapper objectMapper;

    @Autowired
    private UserRepository userRepository;

    @Autowired
    private ProjectRepository projectRepository;

    @Autowired
    private JwtEncoder jwtEncoder;

    @BeforeEach
    void cleanDatabase() {
        projectRepository.deleteAll();
        userRepository.deleteAll();
    }

    @Test
    void healthEndpointIsPublic() throws Exception {
        mockMvc.perform(get("/api/health"))
                .andExpect(status().isOk());
    }

    @Test
    void registrationStoresPasswordHashAndRejectsDuplicateEmail()
            throws Exception {
        String body = """
                {"email":"Alice@Example.com","password":"secure-password-123"}
                """;

        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isCreated())
                .andExpect(jsonPath("$.email").value("alice@example.com"))
                .andExpect(jsonPath("$.passwordHash").doesNotExist());

        var user = userRepository.findByEmail("alice@example.com")
                .orElseThrow();

        org.junit.jupiter.api.Assertions.assertNotEquals(
                "secure-password-123", user.getPasswordHash());
        org.junit.jupiter.api.Assertions.assertTrue(
                user.getPasswordHash().startsWith("$2"));

        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(body))
                .andExpect(status().isConflict());
    }

    @Test
    void loginReturnsBearerTokenAndRejectsWrongPassword()
            throws Exception {
        register("alice@example.com", "secure-password-123");

        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"alice@example.com","password":"wrong-password"}
                                """))
                .andExpect(status().isUnauthorized());

        mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"alice@example.com","password":"secure-password-123"}
                                """))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.accessToken").isNotEmpty())
                .andExpect(jsonPath("$.tokenType").value("Bearer"))
                .andExpect(jsonPath("$.expiresIn").value(3600))
                .andExpect(jsonPath("$.user.passwordHash").doesNotExist());
    }

    @Test
    void projectEndpointsRejectMissingInvalidAndExpiredTokens()
            throws Exception {
        mockMvc.perform(get("/api/projects"))
                .andExpect(status().isUnauthorized());

        mockMvc.perform(get("/api/projects")
                        .header("Authorization", "Bearer not-a-valid-jwt"))
                .andExpect(status().isUnauthorized());

        String expiredToken = createExpiredToken();

        mockMvc.perform(get("/api/projects")
                        .header("Authorization", "Bearer " + expiredToken))
                .andExpect(status().isUnauthorized());
    }

    @Test
    void authenticatedUserCanCreateAndReadOwnProject()
            throws Exception {
        String token = registerAndLogin(
                "alice@example.com", "secure-password-123");

        MvcResult createResult = mockMvc.perform(post("/api/projects")
                        .header("Authorization", "Bearer " + token)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"Alice project","description":"Private project"}
                                """))
                .andExpect(status().isCreated())
                .andReturn();

        JsonNode created = objectMapper.readTree(
                createResult.getResponse().getContentAsString());

        String projectId = created.get("id").asText();

        mockMvc.perform(get("/api/projects/" + projectId)
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Alice project"));

        mockMvc.perform(get("/api/projects")
                        .header("Authorization", "Bearer " + token))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$[0].name").value("Alice project"));
    }

    @Test
    void usersCannotReadUpdateOrDeleteAnotherUsersProject()
            throws Exception {
        String aliceToken = registerAndLogin(
                "alice@example.com", "secure-password-123");

        String bobToken = registerAndLogin(
                "bob@example.com", "another-secure-password-456");

        MvcResult createResult = mockMvc.perform(post("/api/projects")
                        .header("Authorization", "Bearer " + aliceToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"Alice private project","description":"Alice only"}
                                """))
                .andExpect(status().isCreated())
                .andReturn();

        String projectId = objectMapper.readTree(
                        createResult.getResponse().getContentAsString())
                .get("id").asText();

        mockMvc.perform(get("/api/projects/" + projectId)
                        .header("Authorization", "Bearer " + bobToken))
                .andExpect(status().isNotFound());

        mockMvc.perform(put("/api/projects/" + projectId)
                        .header("Authorization", "Bearer " + bobToken)
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"name":"Hijacked project","description":"Changed by Bob"}
                                """))
                .andExpect(status().isNotFound());

        mockMvc.perform(delete("/api/projects/" + projectId)
                        .header("Authorization", "Bearer " + bobToken))
                .andExpect(status().isNotFound());

        // Bob's list must not reveal Alice's project.
        mockMvc.perform(get("/api/projects")
                        .header("Authorization", "Bearer " + bobToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$").isEmpty());

        // Alice's project remains intact.
        mockMvc.perform(get("/api/projects/" + projectId)
                        .header("Authorization", "Bearer " + aliceToken))
                .andExpect(status().isOk())
                .andExpect(jsonPath("$.name").value("Alice private project"));
    }

    @Test
    void invalidRegistrationDataIsRejected() throws Exception {
        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content("""
                                {"email":"not-an-email","password":"short"}
                                """))
                .andExpect(status().isBadRequest());
    }

    private void register(String email, String password) throws Exception {
        mockMvc.perform(post("/api/auth/register")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                java.util.Map.of(
                                        "email", email,
                                        "password", password))))
                .andExpect(status().isCreated());
    }

    private String registerAndLogin(String email, String password)
            throws Exception {
        register(email, password);

        MvcResult result = mockMvc.perform(post("/api/auth/login")
                        .contentType(MediaType.APPLICATION_JSON)
                        .content(objectMapper.writeValueAsString(
                                java.util.Map.of(
                                        "email", email,
                                        "password", password))))
                .andExpect(status().isOk())
                .andReturn();

        return objectMapper.readTree(
                        result.getResponse().getContentAsString())
                .get("accessToken").asText();
    }

    private String createExpiredToken() {
        Instant now = Instant.now();

        JwtClaimsSet claims = JwtClaimsSet.builder()
                .issuer("versionwise")
                .subject(UUID.randomUUID().toString())
                .issuedAt(now.minusSeconds(7200))
                .expiresAt(now.minusSeconds(3600))
                .build();

        return jwtEncoder.encode(
                        JwtEncoderParameters.from(
                                JwsHeader.with(MacAlgorithm.HS256).build(),
                                claims))
                .getTokenValue();
    }
}
