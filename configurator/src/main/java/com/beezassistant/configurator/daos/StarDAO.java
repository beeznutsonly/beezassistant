package com.beezassistant.configurator.daos;

import org.springframework.data.jpa.repository.JpaRepository;
import org.springframework.data.rest.core.annotation.RepositoryRestResource;

import com.beezassistant.configurator.models.DetailedStar;
import com.beezassistant.configurator.models.Star;

@RepositoryRestResource(exported=true, path="stars", excerptProjection = DetailedStar.class)
public interface StarDAO extends JpaRepository<Star, String> {}
