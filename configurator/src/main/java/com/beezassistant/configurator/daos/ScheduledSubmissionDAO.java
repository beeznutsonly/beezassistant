package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.ScheduledSubmission;

@RepositoryRestResource(exported=true, path="scheduledsubmissions")
public interface ScheduledSubmissionDAO extends JpaRepository<ScheduledSubmission, String> {
	
}
