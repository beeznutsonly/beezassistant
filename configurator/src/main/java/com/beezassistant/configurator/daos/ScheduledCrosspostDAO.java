package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.ScheduledCrosspost;
import com.beezassistant.configurator.models.ScheduledCrosspostId;

@RepositoryRestResource(exported=true, path="scheduledcrossposts")
public interface ScheduledCrosspostDAO extends JpaRepository<ScheduledCrosspost, ScheduledCrosspostId> {}