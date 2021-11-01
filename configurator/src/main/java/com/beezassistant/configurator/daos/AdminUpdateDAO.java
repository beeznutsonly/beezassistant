package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.AdminUpdate;

@RepositoryRestResource(exported=true, path="adminupdates")
public interface AdminUpdateDAO extends JpaRepository<AdminUpdate, Integer> {

}
