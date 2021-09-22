package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.AutoCommenter;
import com.beezassistant.configurator.models.AutoCommenterId;

@RepositoryRestResource(exported=true, path="autocomments")
public interface AutoCommenterDAO extends JpaRepository<AutoCommenter, AutoCommenterId> {

}
