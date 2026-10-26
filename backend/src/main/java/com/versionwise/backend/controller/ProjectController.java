
package com.versionwise.backend.controller;

import com.versionwise.backend.dto.CreateProjectRequest;
import com.versionwise.backend.dto.ProjectResponse;
import com.versionwise.backend.service.ProjectService;
import jakarta.validation.Valid;
import org.springframework.http.HttpStatus;
import org.springframework.http.ResponseEntity;
import org.springframework.web.bind.annotation.*;
import java.util.UUID;
import org.springframework.security.core.annotation.AuthenticationPrincipal;
import org.springframework.security.oauth2.jwt.Jwt;
import org.springframework.web.server.ResponseStatusException;
import org.springframework.http.HttpStatus;

import java.net.URI;
import java.util.List;


@RestController
@RequestMapping("/api/projects")
public class ProjectController {

    private final ProjectService projectService;

    public ProjectController(ProjectService projectService) {
        this.projectService = projectService;
    }

    @PostMapping
    public ResponseEntity<ProjectResponse> createProject(
            @Valid @RequestBody CreateProjectRequest request,@AuthenticationPrincipal Jwt jwt
    ) {
        ProjectResponse created = projectService.createProject(request, authenticatedUserId(jwt));

        return ResponseEntity
                .created(URI.create("/api/projects/" + created.id()))
                .body(created);
    }

    @GetMapping
    public List<ProjectResponse> getProjects(@AuthenticationPrincipal Jwt jwt) {
        return projectService.getProjects(authenticatedUserId(jwt));
    }

    @GetMapping("/{id}")
    public ProjectResponse getProject(@PathVariable UUID id,@AuthenticationPrincipal Jwt jwt) {
        return projectService.getProject(id, authenticatedUserId(jwt));
    }

    @PutMapping("/{id}")
    public ProjectResponse updateProject(
            @PathVariable UUID id,
            @Valid @RequestBody CreateProjectRequest request,
            @AuthenticationPrincipal Jwt jwt
    ) {
        return projectService.updateProject(id, request, authenticatedUserId(jwt));
    }

    @DeleteMapping("/{id}")
    @ResponseStatus(HttpStatus.NO_CONTENT)
    public void deleteProject(@PathVariable UUID id,@AuthenticationPrincipal Jwt jwt) {
        projectService.deleteProject(id, authenticatedUserId(jwt));
    }

    private UUID authenticatedUserId(Jwt jwt) {
        try {
            return UUID.fromString(jwt.getClaimAsString("uid"));
        } catch (RuntimeException exception) {
            throw new ResponseStatusException(
                    HttpStatus.UNAUTHORIZED, "Invalid authentication token");
        }
    }
}
