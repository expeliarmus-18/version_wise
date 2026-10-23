
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

    private static final String DEV_EMAIL = "dev@versionwise.local";

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
    public ProjectResponse createProject(CreateProjectRequest request) {
        User owner = getOrCreateDevelopmentUser();

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
    public List<ProjectResponse> getProjects() {
        User owner = getOrCreateDevelopmentUser();

        return projectRepository
                .findByOwnerIdOrderByCreatedAtDesc(owner.getId())
                .stream()
                .map(ProjectResponse::from)
                .toList();
    }

    @Transactional
    public ProjectResponse getProject(UUID id) {
        User owner = getOrCreateDevelopmentUser();
        return ProjectResponse.from(findOwnedProject(id, owner.getId()));
    }

    @Transactional
    public ProjectResponse updateProject(
            UUID id,
            CreateProjectRequest request
    ) {
        User owner = getOrCreateDevelopmentUser();
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
    public void deleteProject(UUID id) {
        User owner = getOrCreateDevelopmentUser();
        Project project = findOwnedProject(id, owner.getId());
        projectRepository.delete(project);
    }

    private User getOrCreateDevelopmentUser() {
        return userRepository.findByEmail(DEV_EMAIL)
                .orElseGet(() ->
                        userRepository.save(new User(DEV_EMAIL)));
    }

    private Project findOwnedProject(UUID projectId, UUID ownerId) {
        return projectRepository.findByIdAndOwner_Id(projectId, ownerId)
                .orElseThrow(() -> new ResponseStatusException(
                        HttpStatus.NOT_FOUND,
                        "Project not found"
                ));
    }
}
