package com.beezassistant.configurator.models;

import java.time.LocalDate;
import java.util.List;

import org.springframework.data.rest.core.config.Projection;

// @Projection(
//     name = "detailed",
//     types = {Star.class}
// )
public interface DetailedStar {
    String getName();
    LocalDate getBirthday();
	String getNationality();
	String getBirthPlace();
	String getYearsActive();
	String getDescription();
    List<StarLink> getStarLinks();
}
