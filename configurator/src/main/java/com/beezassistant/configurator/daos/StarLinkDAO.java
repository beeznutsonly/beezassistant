package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.StarLink;
import com.beezassistant.configurator.models.StarLinkId;

@RepositoryRestResource(exported=true, path="starlinks")
public interface StarLinkDAO extends JpaRepository<StarLink, StarLinkId> {}
