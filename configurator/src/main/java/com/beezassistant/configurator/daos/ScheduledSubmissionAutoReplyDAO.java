package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.ScheduledSubmissionAutoReply;
import com.beezassistant.configurator.models.ScheduledSubmissionAutoReplyId;

@RepositoryRestResource(exported=true, path="scheduledsubmissionautoreplies")
public interface ScheduledSubmissionAutoReplyDAO extends JpaRepository<ScheduledSubmissionAutoReply, ScheduledSubmissionAutoReplyId> {

}
