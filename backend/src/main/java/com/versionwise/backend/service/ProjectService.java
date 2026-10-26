
package com.versionwise.backend.service;

import com.versionwise.backend.dto.CreateProjectRequest;
import com.versionwise.backend.dto.ProjectResponse;
import com.versionwise.backend.entity.Project;
import com.versionwise.backend.entity.User;
import com.versionwise.backend.repository.ProjectRepository;
import com.versionwise.backend.repository.UserRepository;
import org.springframework.http.HttpStatus;
import org.springframework.stereotype.Service;
import org.springframework.transaction.annotation.Transactional;
import org.springframework.web.server.ResponseStatusException;

import java.util.List;
import java.util.UUID;

@Service
public class ProjectService {



    private final ProjectRepository projectRepository;
    private final UserRepository userRepository;

    public ProjectService(
            ProjectRepository projectRepository,
            UserRepository userRepository
    ) {
        this.projectRepository = projectRepository;
        this.userRepository = userRepository;
    }

    @Transactional
    public ProjectResponse createProject(
            CreateProjectRequest request, UUID userId) {
        User owner = getAuthenticatedUser(userId);

        Project project = new Project(
                request.name().trim(),
                request.description() == null
                        ? null
                        : request.description().trim(),
                owner
        );

        return ProjectResponse.from(projectRepository.save(project));
    }

    @Transactional
    public List<ProjectResponse> getProjects(UUID userId) {
        User owner = getAuthenticatedUser(userId);

        return projectRepository.findByOwnerIdOrderByCreatedAtDesc(userId)
                .stream()
                .map(ProjectResponse::from)
                .toList();
    }

    @Transactional
    public ProjectResponse getProject(UUID id,UUID userId) {
        User owner = getAuthenticatedUser(userId);
        return ProjectResponse.from(findOwnedProject(id, owner.getId()));
    }

    @Transactional
    public ProjectResponse updateProject(
            UUID id,
            CreateProjectRequest request,
            UUID userId
    ) {
        User owner = getAuthenticatedUser(userId);
        Project project = findOwnedProject(id, owner.getId());

        project.setName(request.name().trim());
        project.setDescription(
                request.description() == null
                        ? null
                        : request.description().trim()
        );

        return ProjectResponse.from(projectRepository.save(project));
    }

    @Transactional
    public void deleteProject(UUID id,UUID userId) {
        User owner = getAuthenticatedUser(userId);
        Project project = findOwnedProject(id, owner.getId());
        projectRepository.delete(project);
    }


    private User getAuthenticatedUser(UUID userId) {
        return userRepository.findById(userId)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND, "User not found"));
    }



    private Project findOwnedProject(UUID projectId, UUID ownerId) {
        return projectRepository.findByIdAndOwner_Id(projectId, ownerId)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND,
                        "Project not found"
                ));
    }
}
